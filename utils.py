# get origin coordinate of x or y
def get_coord_origin(v: float, ratio: float) -> int:
    """get origin coordinate of x or y

    Args:
        v (float): `x` or `y`
        ratio (flot): _description_

    Returns:
        int: orgin of `x` or `y`
    """
    origin = int(v / ratio)
    
    return origin

def get_lane_divider_x(y, lane_divider_slope, lane_divider_intercept):
    """Draw sloped lane divider based on curb"""
    return int(lane_divider_slope * y + lane_divider_intercept)
    # สมการเส้นตรง y = mx + B (เคสนี้คือ x = my + B)