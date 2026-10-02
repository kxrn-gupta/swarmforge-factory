"""
Unit tests for Stage 4: Production Dark Factory Service & BAND Room Connector.
"""
import unittest
import os
import sys

stage_dir = os.path.dirname(os.path.abspath(__file__))
if stage_dir not in sys.path:
    sys.path.insert(0, stage_dir)

from band_connector import BandDesktopConnector
from factory_server import FactoryHTTPHandler
import json

class TestStage4(unittest.TestCase):
    def test_band_connector_telemetry_export(self):
        connector = BandDesktopConnector(room_id="room-hack-01", room_name="Test Factory")
        connector.log_message(sender="architect-seat", role="Architect", content="Decomposed 4 stages", stage=1)
        connector.log_message(sender="builder-seat", role="Builder", content="Implemented Stage 2", stage=2)
        connector.log_message(sender="verifier-seat", role="Verifier", content="100% tests passed", stage=3)

        telemetry = connector.export_room_telemetry()
        self.assertEqual(telemetry["room_id"], "room-hack-01")
        self.assertEqual(telemetry["total_messages"], 3)
        self.assertEqual(telemetry["status"], "ALL_STAGES_VERIFIED")
        self.assertEqual(telemetry["seats"]["architect"], "Connected")

if __name__ == "__main__":
    unittest.main()
