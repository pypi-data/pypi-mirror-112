import logging
import signal
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import mosaik_api

import rettij
from rettij.common.logging import monitoring_logging
from rettij.common.validated_path import ValidatedFilePath
from rettij.topology.network_components.node import Node

rettij_meta: Dict[str, Any] = {
    "api_version": "2.5",  # compatible with mosaik API version
    "models": {
        "Rettij": {
            "public": True,
            "params": [],  # currently, rettij_mosaik has no model params (only sim params)
            "attrs": [],
        },
        "node": {
            "public": False,
            "params": [],
            "attrs": [],  # these are extended in init() automatically from the topology "data" keys for the nodes
        },
    },
    "extra_methods": [
        "connect",
    ],
}
logger = logging.getLogger("mosaik.rettij")


class RettijMosaik(mosaik_api.Simulator):
    """
    This class serves as a wrapper for using rettij with the mosaik co-simulator.

    It mostly handles data parsing for the mosaik meta model.
    Other function calls are generally passed directly to rettij.
    """

    def __init__(self, meta: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the RettijMosaik wrapper.

        :param meta: (Optional) Mosaik meta model. If not specified,  a default rettij meta model is
                     used. It can be specified as a parameter, so one can implement this class and override it with
                     `super().__init__(meta)` and pass a custom meta model.
        """
        if not meta:
            meta = rettij_meta
        super().__init__(meta)

        self.eid: str = ""
        self.rettij: Optional[rettij.Rettij] = None

        # configure SIGINT signal handler, so the user can stop rettij by CTRL+C
        signal.signal(signal.SIGINT, self.handle_interrupt)

    def init(self, sid: str, **sim_params: Any) -> Any:
        """
        Initialize the SimRettij mosaik simulator and rettij.

        Implements mosaik `init()` method.

        :param sid: Simulator id.
        :param sim_params: Simulator parameters.
        :return: Mosaik meta model.
        """
        constructor_params: dict = {}
        if sim_params.get("file_loglevel"):
            constructor_params["file_loglevel"] = sim_params["file_loglevel"]
        if sim_params.get("console_loglevel"):
            constructor_params["console_loglevel"] = sim_params["console_loglevel"]

        init_params: dict = {}
        if sim_params.get("topology_path"):
            init_params["topology_path"] = ValidatedFilePath(sim_params["topology_path"])
        else:
            raise ValueError("'topology_path' is a required parameter for RettijMosaik!")
        if sim_params.get("sequence_path"):
            init_params["sequence_path"] = Path(sim_params["sequence_path"])
        if sim_params.get("kubeconfig_path"):
            init_params["kubeconfig_path"] = Path(sim_params["kubeconfig_path"])
        if sim_params.get("components_dir_path"):
            init_params["components_dir_path"] = Path(sim_params["components_dir_path"])
        if sim_params.get("step_size"):
            init_params["step_size"] = sim_params["step_size"]
        if sim_params.get("monitoring_config"):
            init_params["monitoring_config"] = sim_params["monitoring_config"]
            monitoring_logging.get_logger(sim_params["monitoring_config"])

        # init rettij
        self.rettij = rettij.Rettij(**constructor_params)
        self.rettij.init(**init_params)

        # collect available attributes of rettij nodes (they are defined in the topology file under the "data" key)
        node_data_attributes = set()  # use a set because it can't hold the same item twice
        for node_id, node in self.rettij.nodes.items():
            try:
                node_data_attributes.update(node.data.keys())  # insert keys into list
            except AttributeError:
                continue
        self.meta["models"]["node"]["attrs"].extend(list(node_data_attributes))

        return self.meta

    def create(self, num: int, model: str, **model_params: Any) -> List[Dict]:
        """
        Create the SimRettij mosaik simulator and the rettij simulation.

        Implements the mosaik `create()` method.

        Known limitations: Only one rettij model can be created (there was no use-case for multiple ones, yet).

        :param num: Number of instances to create.
        :param model: Model to create.
        :param model_params: Model parameters (meta['models'][model]['params']).
        :return: Return list with entitiy dicts created for the simulation.
        """
        if not self.rettij:
            raise RuntimeError("rettij not initialized, please run 'init()' first!")

        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one instance of rettij.")

        self.eid = f"{model}-0"

        self.rettij.create()

        children: List[Dict] = self.create_children()
        model_instances: List[Dict] = [
            {
                "eid": self.eid,
                "type": model,
                "children": children,
            }
        ]

        return model_instances

    def create_children(self) -> List[Dict]:
        """
        Create children for the mosaik model.

        :return: Return children entities for rettij mosaik model.
        """
        if not self.rettij:
            raise RuntimeError("rettij not initialized, please run 'init()' first!")

        children = []

        for node_eid in self.rettij.sm.nodes:
            node_entity = self.create_entity(node_eid, "node")
            children.append(node_entity)

        return children

    def create_entity(self, eid: str, entity_type: str) -> Dict:
        """
        Create a single mosaik entity, which basically is a dict with some essential predefined fields.

        :param eid: entity id of the new entity
        :param entity_type: entity type
        :return: new entity object (basically a a dict with some mandatory fields)
        """
        possible_entity_types = self.meta["models"].keys()
        if entity_type not in possible_entity_types:
            logger.error(f"Invalid entity type '{entity_type}', must be one of {possible_entity_types}.")
            sys.exit(1)
        entity = {
            "eid": eid,
            "type": entity_type,
            "children": [],
            "rel": [],  # relations are empty for now; not sure if this would really help anywhere
        }
        return entity

    def connect(self, source_node: Node, target_node: Node, **kwargs: Any) -> None:
        """
        Connect one Node to another.

        The method is meant to be used to establish a logical, one way data connection between two Nodes, where the source node sends certain attribute values to the target node.
        Calls the respective components 'connect' hooks.

        :param source_node: Base Node that the connection is initiated on.
        :param target_node: Node to connect the base Node to.
        :param kwargs: Custom parameters. Contents depend on the specific implementation.
        """
        if not self.rettij:
            raise RuntimeError("rettij not initialized, please run 'init()' first!")
        self.rettij.connect(source_node, target_node, **kwargs)

    def step(self, sim_time: int, inputs: Dict[str, Any]) -> int:
        """
        Run a single step.

        Will always sleep for one second after executing the step to account for data propagation through the simulated real-time network.
        :param sim_time: Current simulation time, i.e. at which the step should be simulated with.
        :param inputs: Inputs to the step. Example: `{'n305': {'closed': {'SimPowerSwitch-0.Model_power_switch_0': True}}}`
        :return: Next simulation time that rettij.step() should be called at.
        """
        if not self.rettij:
            raise RuntimeError("rettij not initialized, please run 'init()' and 'create()' first!")
        next_step_time = self.rettij.step(sim_time, inputs)
        time.sleep(1)
        return next_step_time

    def get_data(self, outputs: Dict[str, List[str]]) -> Dict[str, Dict[str, Any]]:
        """
        Get data from nodes. Implements mosaik API method get_data.

        :param outputs: Requested outputs, looks like this: {'n305': ['closed']})
        :return: Requested data from nodes, e.g.: {"n305": {"closed": True}}
        """
        if not self.rettij:
            raise RuntimeError("rettij not initialized, please run 'init()' and 'create()' first!")
        return self.rettij.get_data(outputs)

    def finalize(self) -> None:
        """
        Finalize the simulation.
        """
        if self.rettij:
            self.rettij.finalize()

    def handle_interrupt(self, _signal: Any, _frame: Any) -> None:
        """
        Handle ctrl+c interrupt and finalize the simulation.
        """
        self.finalize()
