import importlib
import importlib.util
import os
import tempfile
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Any, Optional, List

import kubernetes

from rettij.abstract_scheduled_sequence import AbstractScheduledSequence
from rettij.abstract_script_sequence import AbstractScriptSequence
from rettij.commands.command import Command
from rettij.commands.command_result import CommandResult
from rettij.common.constants import COMPONENTS_DIR
from rettij.common.logging_utilities import LoggingSetup, Loglevel
from rettij.common.validated_path import ValidatedDirPath, ValidatedFilePath
from rettij.exceptions.invalid_path_exception import InvalidPathException
from rettij.simulation_manager import SimulationManager
from rettij.topology.exec_result import ExecResult
from rettij.topology.network_components.channel import Channel
from rettij.topology.network_components.node import Node
from rettij.topology.node_container import NodeContainer
from rettij.topology.node_executors.dummy_executor import DummyExecutor
from rettij.topology.topology_exporter_mermaid import TopologyExporterMermaid
from rettij.topology.topology_reader import TopologyReader


class Rettij:
    """
    Main Rettij class.
    """

    # Event for when there are no more steps to execute
    no_more_steps_event: threading.Event = threading.Event()

    def __init__(
        self,
        file_loglevel: Loglevel = Loglevel.INFO,
        console_loglevel: Loglevel = Loglevel.WARNING,
        fail_on_step_error: bool = True,
    ):
        """
        Create a Rettij object that is used to use Rettij itself.

        :param file_loglevel: (Optional) File loglevel. Default: INFO
        :param console_loglevel: (Optional) Console loglevel. Default: WARNING
        :param fail_on_step_error: (Optional) If True, raise exception on step execution failure. If False, continue execution.
        """
        self.uid: str = str(datetime.now().strftime("%Y%m%d-%H%M%S"))  # create (almost) unique id from timestamp
        self.fail_on_step_error: bool = fail_on_step_error
        self.is_finalized: bool = False

        LoggingSetup.initialize_logging(self.uid, file_loglevel, console_loglevel)
        self.logger = LoggingSetup.submodule_logging(self.__class__.__name__)

        self.sm: SimulationManager = SimulationManager(self.uid)
        self.sequence: Optional[AbstractScheduledSequence] = None

        # Simulation time increment for each step
        self.step_size: int = 1

    def __load_topology(
        self, topology_path: ValidatedFilePath, components_dir_path: ValidatedDirPath = ValidatedDirPath(COMPONENTS_DIR)
    ) -> None:
        """
        Load the simulation topology from a file.

        RETTIJ INTERNAL USE ONLY. rettij does not support loading a new topology after the initial deployment.

        :param topology_path: Validated Path to the file containing the topology.
        :param components_dir_path: (Optional) Path to the directory containing custom components.
        """
        self.logger.info("Loading simulation topology from {}".format(topology_path))
        topo_reader: TopologyReader = TopologyReader()
        nodes, channels = topo_reader.read(topology_path, components_dir_path)
        self.nodes.update(nodes)
        self.channels.update(channels)

    def load_sequence(self, sequence_path: Path) -> None:
        """
        Load a simulation sequence from a file.

        :param sequence_path: Path to the file containing the simulation sequence.
        """
        self.logger.info("Loading simulation sequence from {}".format(sequence_path))
        spec = importlib.util.spec_from_file_location("sequence", str(sequence_path))
        sequence_module = importlib.util.module_from_spec(spec)
        # We have to ignore the reference errors in the following code since it's a bit hacked together
        # noinspection PyUnresolvedReferences
        spec.loader.exec_module(sequence_module)  # type: ignore
        # noinspection PyUnresolvedReferences
        if hasattr(sequence_module, "ScheduledSequence"):
            sequence: sequence_module.ScheduledSequence = sequence_module.ScheduledSequence()  # type: ignore
        elif hasattr(sequence_module, "ScriptSequence"):
            sequence: sequence_module.ScriptSequence = sequence_module.ScriptSequence()  # type: ignore
        else:
            raise AttributeError("module 'sequence' has no attribute 'ScheduleSequence' or 'ScriptSequence'")
        self.sequence = sequence
        if isinstance(self.sequence, AbstractScheduledSequence):
            self.run_sequence()
        elif isinstance(self.sequence, AbstractScriptSequence):
            self.sm.add_step(
                scheduled_time=self.sm.current_time + 1,
                command=self.run_sequence,
            )
        else:
            raise TypeError(
                "Sequence must be of type 'rettij.AbstractScheduledSequence' or 'rettij.AbstractScriptSequence'!"
            )

    class RunSequenceCommand(Command):
        """
        This Command class is used to define (execute) a sequence for rettij.
        """

        def __init__(self, rettij: Any):
            """
            Initialize a RunSequenceCommand object.

            :param rettij: Rettij object (annotated as 'Any' for import order reasons)
            """
            self.rettij = rettij
            super().__init__(DummyExecutor("rettij"), [])

        def execute(self, current_time: int = 0, inputs: Optional[Dict] = None) -> CommandResult:
            """
            Define the sequence for rettij.

            :param current_time: Not used, default '0'.
            :param inputs: Not used, default 'None'.
            :return: CommandResult object.
            """
            self.rettij.sequence.define(
                self.rettij.sm, self.rettij.nodes, self.rettij.nodes, self.rettij.channels, self.rettij.channels
            )
            self.result = CommandResult(ExecResult())
            return self.result

    def run_sequence(self, exec_now: bool = True) -> Command:
        """
        Create (and execute) a RunSequenceCommand.

        :param exec_now: Execute the command immediately if 'True'. Else, return the Command object without executing it. Default: 'True'.
        :return: RunSequenceCommand object.
        """
        cmd = self.RunSequenceCommand(self)
        if exec_now:
            cmd.execute()
        return cmd

    def init(
        self,
        topology_path: ValidatedFilePath,
        sequence_path: Optional[Path] = None,
        kubeconfig_path: Optional[Path] = None,
        components_dir_path: Optional[Path] = Path(COMPONENTS_DIR),
        mermaid_export_path: Optional[Path] = None,
        step_size: int = 1,
        callback: Optional[Callable[[], None]] = None,
    ) -> None:
        """
        Initialize the simulator.

        :param topology_path: (Validated) Path to the file containing the topology.
        :param sequence_path: (Optional) Path to the file containing the simulation sequence.
        :param kubeconfig_path: (Optional) Path to the file containing the `kubeconfig` file.
        :param components_dir_path: (Optional) Path to the directory containing custom components. Default: rettij built-in components directory.
        :param mermaid_export_path: (Optional) Path for the mermaid topology export file.
        :param step_size: (Optional) Simulation step size, which is the simulation time increment for each step. Default: `1`.
        :param callback: (Optional) Callback function to be run when the simulation configuration has been parsed.
        """
        # Verify inputs. As this method is used externally, we cannot rely that the input parameters are valid.
        if not isinstance(topology_path, ValidatedFilePath):
            raise AttributeError("Parameter 'topology_path' must be of type 'ValidatedFilePath'.")
        if sequence_path and not isinstance(sequence_path, Path):
            raise AttributeError("Parameter 'sequence_path' must be of type 'Path'.")
        if kubeconfig_path and not isinstance(kubeconfig_path, Path):
            raise AttributeError("Parameter 'kubeconfig_path' must be of type 'Path'.")
        if components_dir_path and not isinstance(components_dir_path, Path):
            raise AttributeError("Parameter 'components_dir_path' must be of type 'Path'.")
        if mermaid_export_path and not isinstance(mermaid_export_path, Path):
            raise AttributeError("Parameter 'mermaid_export_path' must be of type 'Path'.")
        if step_size:
            if not isinstance(step_size, int):
                raise AttributeError("Parameter 'step_size' must be of type 'int'.")
            if step_size < 1:
                raise ValueError("Parameter 'step_size' must be >= 1.")
        if callback and not isinstance(callback, Callable):  # type: ignore
            # Ignore the mypy check because of https://github.com/python/mypy/issues/6864
            raise AttributeError("Parameter 'callback' must be of type 'Callable[[], None]'.")

        try:
            kubeconfig_loaded: bool = False
            kubeconfig_default_path: Path = Path.home() / ".kube" / "config"

            # Try loading kubeconfig from kubeconfig_path parameter
            if not kubeconfig_loaded and kubeconfig_path:
                try:
                    self.logger.info(f"Loading kubeconfig from {kubeconfig_path} ...")
                    kubernetes.config.load_kube_config(ValidatedFilePath(kubeconfig_path))
                    kubeconfig_loaded = True
                except InvalidPathException as e:
                    self.logger.warning(f"No kubeconfig file found at {e.path_normalized}")

            # Try loading kubeconfig from value of KUBECONFIG environment variable (path to kubeconfig file)
            if not kubeconfig_loaded:
                try:
                    self.logger.info("Loading kubeconfig file path from KUBECONFIG environment variable...")
                    kubeconfig_path = Path(os.environ["KUBECONFIG"])
                    kubernetes.config.load_kube_config(ValidatedFilePath(kubeconfig_path))
                    kubeconfig_loaded = True
                except KeyError:
                    self.logger.warning("Environment variable KUBECONFIG not set.")
                except InvalidPathException as e:
                    self.logger.warning(f"No kubeconfig file found at {e.path_normalized}")

            # Try loading kubeconfig from default path
            if not kubeconfig_loaded:
                try:
                    self.logger.info(f"Loading kubeconfig from default path {kubeconfig_default_path} ...")
                    kubernetes.config.load_kube_config(ValidatedFilePath(str(kubeconfig_default_path)))
                    kubeconfig_loaded = True
                except InvalidPathException as e:
                    self.logger.warning(f"No kubeconfig file found at {e.path_normalized}")

            # Try loading cluster access information from KUBE_TOKEN, KUBE_URL and KUBE_CA_PEM (path to ca certificate pem file) environment variables
            # This is used for the CI pipeline
            if not kubeconfig_loaded:
                try:
                    self.logger.info("Loading cluster access information from environment variables ...")
                    configuration = kubernetes.client.Configuration()

                    configuration.api_key["authorization"] = os.environ["KUBE_TOKEN"]
                    configuration.api_key_prefix["authorization"] = "Bearer"
                    configuration.host = os.environ["KUBE_URL"]
                    configuration.ssl_ca_cert = os.environ["KUBE_CA_PEM"]

                    kubernetes.client.Configuration.set_default(configuration)
                    kubeconfig_loaded = True
                except KeyError:
                    self.logger.warning("Environment variables KUBE_TOKEN/KUBE_URL/KUBE_CA_PEM not set.")

            if not kubeconfig_loaded:
                raise RuntimeError("Unable to load Kubernetes cluster access information.")

            self.logger.info(f"Using kubernetes url '{kubernetes.client.ApiClient().configuration.host}'.")

            self.__load_topology(topology_path, ValidatedDirPath(components_dir_path))

            # export topology as mermaid graph
            if not mermaid_export_path:
                mermaid_export_path = Path(tempfile.mkdtemp()) / "mermaid_topology.txt"
            topo_exporter_mermaid: TopologyExporterMermaid = TopologyExporterMermaid(self.nodes, self.channels)
            topo_exporter_mermaid.export(mermaid_export_path)

            # Load the simulation sequence
            if sequence_path:
                self.load_sequence(sequence_path)

            self.step_size = step_size

            if callback:
                callback()

        except Exception as e:
            self._handle_error(e)

    def create(
        self,
        callback: Optional[Callable[[], None]] = None,
    ) -> None:
        """
        Create the simulation components.

        :param callback: (Optional) Callback function to be run when the simulation components have been created.
        :raises: RettijRuntimeException.
        """
        # Verify inputs. As this method is used externally, we cannot rely that the input parameters are valid.
        if callback and not isinstance(callback, Callable):  # type: ignore
            # Ignore the mypy check because of https://github.com/python/mypy/issues/6864
            raise AttributeError("Parameter 'callback' must be of type 'Callable[[], None]'.")

        try:
            self.logger.info("Setting up simulation environment (may take up to a minute)...")

            self.sm.kubernetes_api = kubernetes.client.CoreV1Api()
            self.sm.create_simulation()

            if callback:
                callback()

        except Exception as e:
            self._handle_error(e)

    def step(
        self,
        current_time: int,
        inputs: dict,
        callback: Optional[Callable[[], None]] = None,
    ) -> int:
        """
        Execute a simulation step.

        :param current_time: Current time of the external co-simulator.
        :param inputs: Dict of inputs for the current step A dict of dicts mapping entity IDs to attributes of the simulation components.
        :param callback: (Optional) Callback function to be run once a step has finished.
        :raises: RettijRuntimeException
        :return: Next time rettij wants to be called (always the current_time plus the step_size, which defaults to 1).
        """
        # Verify inputs. As this method is used externally, we cannot rely that the input parameters are valid.
        if not isinstance(current_time, int):
            raise AttributeError("Parameter 'current_time' must be of type 'int'.")
        if not isinstance(inputs, dict):
            raise AttributeError("Parameter 'inputs' must be of type 'dict'.")
        if callback and not isinstance(callback, Callable):  # type: ignore
            # Ignore the mypy check because of https://github.com/python/mypy/issues/6864
            raise AttributeError("Parameter 'callback' must be of type 'Callable[[], None]'.")

        try:
            self.sm.step(current_time, inputs, self.fail_on_step_error)
            if callback:
                callback()
        except Exception as e:
            self._handle_error(e)

        # Return the minimum time increase as new scheduled time until the simulation end
        return current_time + self.step_size

    def get_data(self, outputs: Dict[str, List]) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Retrieve output data from the simulation.

        Delegates to the corresponding method in SimulationManager.

        :param outputs: Attributes to be retrieved and returned. Format: {'n305': ['closed', 'active']}
        :return: Requested output data. Format: {'n305': {'closed': True, 'active': False}}
        """
        # Verify inputs. As this method is used externally, we cannot rely that the input parameters are valid.
        if not isinstance(outputs, dict):
            raise AttributeError("Parameter 'outputs' must be of type 'dict'.")

        return self.sm.get_data(outputs)

    def has_next_step(self, current_time: int) -> bool:
        """
        Check if there are more steps to execute for the Simulator.

        :return: True if more steps are present, false if not.
        """
        return self.sm.has_next_step(current_time)

    def connect(self, source_node: Node, target_node: Node, **kwargs: Any) -> None:
        """
        Connect one Node to another.

        The method is meant to be used to establish a logical, one way data connection between two Nodes, where the source node sends certain attribute values to the target node.
        Calls the respective components 'connect' hooks.

        :param source_node: Base Node that the connection is initiated on.
        :param target_node: Node to connect the base Node to.
        :param kwargs: Custom parameters. Contents depend on the specific implementation.
        """
        # Verify inputs. As this method is used externally, we cannot rely that the input parameters are valid.
        if not isinstance(source_node, Node):
            raise AttributeError("Parameter 'source_node' must be of type 'Node'.")
        if not isinstance(target_node, Node):
            raise AttributeError("Parameter 'target_node' must be of type 'Node'.")

        self.sm.connect(source_node, target_node, **kwargs)

    def finalize(
        self,
        callback: Optional[Callable[[], None]] = None,
    ) -> None:
        """
        Stop the simulation and clean up all components.

        :param callback: Callback function to be run once the simulation has been taken down.
        """
        # Verify inputs. As this method is used externally, we cannot rely that the input parameters are valid.
        if callback and not isinstance(callback, Callable):  # type: ignore
            # Ignore the mypy check because of https://github.com/python/mypy/issues/6864
            raise AttributeError("Parameter 'callback' must be of type 'Callable[[], None]'.")

        self.logger.info("Finalizing as soon as possible...")
        # if something like reading the input files failed, there might be no sm-object to delete
        if self.sm is not None:
            self.sm.cleanup(f"rettij-{self.uid}")
        self.logger.info("Finalization complete.")

        self.is_finalized = True

        if callback:
            callback()

    def _handle_error(self, exception: Exception) -> None:
        """
        Handle errors during rettij execution.
        """
        if not self.is_finalized:
            self.logger.critical("Critical error encountered! Triggering phase FINALIZE.")
            self.finalize()
        raise exception

    def __del__(self) -> None:
        if not self.is_finalized:
            self.finalize()

    @property
    def nodes(self) -> NodeContainer:
        """
        Retrieve the simulation Nodes.

        :return: NodeContainer with the simulation Nodes.
        """
        return self.sm.nodes

    @property
    def channels(self) -> Dict[str, Channel]:
        """
        Retrieve the simulation Channels.

        :return: Dictionary with the simulation Channels. Format: {'c1': Channel}
        """
        return self.sm.channels
