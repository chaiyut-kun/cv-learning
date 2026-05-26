import unittest
from utils import get_coord_origin, get_lane_divider_x

class TestGetCoordOrigin(unittest.TestCase):

    def test_positive_values(self):
        """Test with positive v and ratio."""
        self.assertEqual(get_coord_origin(100, 0.5), 200)
        self.assertEqual(get_coord_origin(50, 0.25), 200)
        self.assertEqual(get_coord_origin(10, 2), 5)

    def test_zero_v(self):
        """Test when v is zero."""
        self.assertEqual(get_coord_origin(0, 0.5), 0)
        self.assertEqual(get_coord_origin(0, 1), 0)

    def test_negative_values(self):
        """Test with negative v or ratio."""
        self.assertEqual(get_coord_origin(-100, 0.5), -200)
        self.assertEqual(get_coord_origin(100, -0.5), -200)
        self.assertEqual(get_coord_origin(-100, -0.5), 200)

    def test_float_result_truncation(self):
        """Test that the result is truncated to an integer."""
        self.assertEqual(get_coord_origin(10, 3), 3) # 10 / 3 = 3.33 -> 3
        self.assertEqual(get_coord_origin(9, 2), 4)  # 9 / 2 = 4.5 -> 4

    def test_zero_ratio_raises_error(self):
        """Test that ZeroDivisionError is raised when ratio is zero."""
        with self.assertRaises(ZeroDivisionError):
            get_coord_origin(100, 0)

class TestGetLaneDividerX(unittest.TestCase):
    def test_positive_values(self):
        self.assertEqual(get_lane_divider_x(y=100, lane_divider_slope=0.5, lane_divider_intercept=10), 60) # 0.5 * 100 + 10 = 60
        self.assertEqual(get_lane_divider_x(y=50, lane_divider_slope=2, lane_divider_intercept=5), 105) # 2 * 50 + 5 = 105

    def test_negative_slope(self):
        self.assertEqual(get_lane_divider_x(y=100, lane_divider_slope=-0.5, lane_divider_intercept=100), 50) # -0.5 * 100 + 100 = 50
        self.assertEqual(get_lane_divider_x(y=200, lane_divider_slope=-1, lane_divider_intercept=300), 100) # -1 * 200 + 300 = 100

    def test_zero_slope(self):
        self.assertEqual(get_lane_divider_x(y=100, lane_divider_slope=0, lane_divider_intercept=50), 50) # 0 * 100 + 50 = 50

    def test_zero_intercept(self):
        self.assertEqual(get_lane_divider_x(y=100, lane_divider_slope=0.5, lane_divider_intercept=0), 50) # 0.5 * 100 + 0 = 50

    def test_float_result_truncation(self):
        self.assertEqual(get_lane_divider_x(y=10, lane_divider_slope=1.5, lane_divider_intercept=0), 15) # 1.5 * 10 + 0 = 15.0 -> 15
        self.assertEqual(get_lane_divider_x(y=3, lane_divider_slope=3.33, lane_divider_intercept=0), 9) # 3.33 * 3 + 0 = 9.99 -> 9

if __name__ == '__main__':
    unittest.main()