import unittest
from datetime import datetime
from typing import Tuple
from unittest.mock import ANY

from .test_sdk import _simple_binary_model

import pytest

import feyn


def make_node(ix: int, spec: str, location: Tuple[int, int, int], name=""):
    return {
        "id": ix,
        "spec": spec,
        "location": list(location),
        "peerlocation": list(location),
        "name": name,
        "state": {},
    }


@pytest.mark.integration
class TestSnapshots(unittest.TestCase):
    def setUp(self):
        self.lt = feyn.connect_qlattice()
        self.lt.reset()

    # TODO: Finish your project about auto-checking for docstrings during a release
    def test_can_capture_a_snapshot(self):
        snapshot_info = self.lt.snapshots.capture("My lovely QLattice")

        self.assertEqual(snapshot_info.id, ANY)
        self.assertAlmostEqual(
            snapshot_info.when.timestamp(), datetime.now().timestamp(), places=-1
        )
        self.assertEqual(snapshot_info.note, "My lovely QLattice")

    def test_can_list_snapshots(self):
        self.lt.snapshots.capture("Snapshot #1")
        self.lt.snapshots.capture("Snapshot #2")
        self.lt.snapshots.capture("Snapshot #3")

        with self.subTest("Should have three snapshots"):
            self.assertGreater(len(self.lt.snapshots), 2)

        with self.subTest("should be ordered with most recent last"):
            self.assertEqual(self.lt.snapshots[-1].note, "Snapshot #3")

    def test_can_restore_snapshot(self):

        # Create a graph and update the QLattice to create the registers
        m = _simple_binary_model()
        self.lt.update(m)

        snapshot = self.lt.snapshots.capture("testing")
        with self.subTest("Can restore with snapshot instance"):
            self.lt.reset()
            self.assertEqual(len(self.lt.registers), 0)

            self.lt.snapshots.restore(snapshot)
            self.assertEqual(len(self.lt.registers), 3)

        with self.subTest("Can restore with snapshot id"):
            self.lt.reset()
            self.assertEqual(len(self.lt.registers), 0)

            self.lt.snapshots.restore(snapshot.id)
            self.assertEqual(len(self.lt.registers), 3)

        with self.subTest("Fails gracefully on non-existent id"):
            with self.assertRaises(ValueError):
                self.lt.snapshots.restore("non-existent-id")
