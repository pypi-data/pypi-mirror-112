from weightsplitter.main import WeightSplitter
import unittest


class MainTest(unittest.TestCase):
    def test_get_test_value(self):
        ws = WeightSplitter('0.0.0.0', 1337, debug=True, test_mode=True, test_value='10101010')
        ws.start()

if __name__ == '__main__':
    unittest.main()
