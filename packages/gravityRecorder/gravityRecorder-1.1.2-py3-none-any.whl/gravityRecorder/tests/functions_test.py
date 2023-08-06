import unittest
from gravityRecorder import functions


class FunctionsTest(unittest.TestCase):
    def test_reg_act_to_pol(self):
        functions.register_act_to_polygon(1,178)