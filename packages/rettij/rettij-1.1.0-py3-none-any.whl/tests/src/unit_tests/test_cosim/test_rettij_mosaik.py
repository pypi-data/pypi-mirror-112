import unittest
from pathlib import Path
from unittest.mock import MagicMock

from rettij import Rettij
from rettij.common.constants import SRC_DIR, TESTS_DIR
from rettij.common.logging_utilities import Loglevel
from rettij.cosim.rettij_mosaik import RettijMosaik
from rettij.topology.node_container import NodeContainer


class TestRettijMosaik(unittest.TestCase):
    """
    This TestCase contains unit tests regarding the RettijMosaik class.
    """

    def setUp(self) -> None:
        """
        Set up the TestCase instance variables.
        """
        self.rettij_mosaik: RettijMosaik = RettijMosaik()

    def test_init(self) -> None:
        """
        Verify that RettijMosaik.init() works with valid parameters.
        """
        rettij_params = {
            "sim_name": "SimRettij",
            "step_size": 1,
            "file_loglevel": Loglevel.DEBUG,
            "console_loglevel": Loglevel.INFO,
            "topology_path": Path(SRC_DIR) / "examples" / "topologies" / "simple-switch_topology.yml",
            "sequence_path": "",
            "components_dir_path": Path(TESTS_DIR) / "shared_resources" / "custom_components",
            "kubeconfig_path": "",
            "monitoring_config": "",
        }

        self.rettij_mosaik.init("", **rettij_params)

        self.assertIsInstance(self.rettij_mosaik.rettij, Rettij)
        assert isinstance(self.rettij_mosaik.rettij, Rettij)
        self.assertGreater(len(self.rettij_mosaik.rettij.nodes), 0)

    def test_create_children(self) -> None:
        """
        Verify that `RettijMosaik.create_children()` returns the expected data.

        Implicitly tests `RettijMosaik.create_entity()` as well, as it is called by `RettijMosaik.create_children()`.
        """
        n0 = MagicMock()
        n1 = MagicMock()
        nodes = {"n0": n0, "n1": n1}
        node_container = NodeContainer(nodes)
        self.rettij_mosaik.rettij = MagicMock()
        self.rettij_mosaik.rettij.sm = MagicMock()
        self.rettij_mosaik.rettij.sm.nodes = node_container
        children = self.rettij_mosaik.create_children()

        # Using output from `self.rettij_mosaik.create_children()` to ensure future consistency of data
        self.assertEqual(
            children,
            [
                {"eid": "n0", "type": "node", "children": [], "rel": []},
                {"eid": "n1", "type": "node", "children": [], "rel": []},
            ],
        )

    # RettijMosaik.create() requires a live system and is not unit testable with any meaningful result
    # RettijMosaik.connect() requires a live system and is not unit testable with any meaningful result
    # RettijMosaik.step() requires a live system and is not unit testable with any meaningful result
    # RettijMosaik.get_data() requires a live system and is not unit testable with any meaningful result
    # RettijMosaik.finalize() requires a live system and is not unit testable with any meaningful result
