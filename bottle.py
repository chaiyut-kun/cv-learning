import cv2 as cv
from ultralytics import YOLO

window_name = "Yolo car cout"

model = YOLO('yolo12l.pt')
class_list = model.names

cap = cv.VideoCapture('assets/test-bottle.mp4')
cv.namedWindow(window_name)

ratio = 0.4

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Video has issue")
        break
    
    # cal new height for scale down resolution
    new_height = int(frame.shape[0] * ratio)
    new_width = int(frame.shape[1] * ratio)
    
    # persist True = แทรกตัววัตถุไปเรื่อยๆ
    results = model.track(frame, persist=True, classes=[39], device='cpu', verbose=False)
    if results[0].boxes.data is not None:
        
        result = results[0].boxes
        
        boxes = result.xyxy.cpu()
        track_ids = result.id.int().cpu().tolist()
        class_indices = result.cls.int().cpu().tolist()
        confidences = result.conf.cpu()
        
    for box, track_id, class_idx, conf in zip(boxes, track_ids, class_indices, confidences):
        # split coordinates
        x1, y1, x2, y2 = map(int, box)
        
        # config center of object
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        # map class name with class list dict
        class_name = class_list[class_idx]

        # track center of object
        cv.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)

        cv.putText(frame, f"ID: {track_id} - {class_name}", (x1, y1 - 10), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255))
        
        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    scaled_frame = cv.resize(frame, (new_width, new_height))
    cv.imshow(window_name, scaled_frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()