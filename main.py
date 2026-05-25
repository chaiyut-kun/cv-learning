import cv2 as cv
from ultralytics import YOLO

# mouse callback function to get image coordinate
def mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # convert scaled coordinates to original
        orgin_x = int(x / ratio)
        orgin_y = int(y / ratio)
        print(f"Mouse clicked at: X={orgin_x}, Y={orgin_y}")

def get_lane_divider_x(y):
    """Draw sloped lane divider based on curb"""
    return int(lane_divider_slope * y + lane_divider_intercept)

def draw_sloped_lane_divider(frame, y_start, y_end):
    x_start = get_lane_divider_x(y_start)
    x_end = get_lane_divider_x(y_end)
    cv.line(frame, (x_start, y_start), (x_end, y_end), (255,255,255), 3)


ratio = 0.5
line_y_in = 1300
line_y_out = line_y_in
lane_divider_slope = 0.409
lane_divider_intercept = 1459.6
divider_x_at_out = get_lane_divider_x(line_y_out)
divider_x_at_in = get_lane_divider_x(line_y_in)