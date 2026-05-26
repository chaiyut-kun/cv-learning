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
    # สมการเส้นตรง y = mx + B (เคสนี้คือ x = my + B)

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

# Load YOLO Model
model = YOLO('yolo12l.pt')
class_list = model.names

# อ่าน vdo
cap = cv.VideoCapture('vehicle-count.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Video has issue")
        break
    
    # cal new height for scale down resolution
    new_height = int(frame.shape[0] * ratio)
    new_width = int(frame.shape[1] * ratio)
    
    # persist True = แทรกตัววัตถุไปเรื่อยๆ
    results = model.track(frame, persist=True, classes=[2, 7], device='cpu', verbose=False)
    if results[0].boxes.data is not None:
        
        result = results[0].boxes
        
        boxes = result.xyxy.cpu()
        track_ids = result.id.int().cpu().tolist()
        class_indices = result.cls.int().cpu().tolist()
        confidences = result.conf.cpu()
        
    for box, track_id, class_idx, conf in zip(boxes, track_ids, class_indices, confidences):
        x1, y1, x2, y2 = map(int, box)

        class_name = class_list[class_idx]
        cv.putText(frame, f"ID: {track_id} - {class_name}", (x1, y1 - 10), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255))
        
        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    scaled_frame = cv.resize(frame, (new_width, new_height))
    cv.imshow("frame of vdo", scaled_frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()