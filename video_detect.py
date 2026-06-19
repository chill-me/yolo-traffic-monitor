from ultralytics import YOLO
import cv2
import csv
from datetime import datetime
import os
import pandas as pd

csv_file = "traffic_log.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "id",
            "type"
        ])

model = YOLO("yolo11n.pt")

video_path = "132849-754950619_tiny.mp4"

cap = cv2.VideoCapture(video_path)

LINE_Y = 400
previous_positions = {}
counted_ids = set()
total_count = 0


while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    results = model.track(
        frame, 
        persist=True
    )

    person_count = 0
    car_count = 0
    boxes = results[0].boxes

    if boxes.id is not None:
        for box, id, cls in zip(
            boxes.xyxy, 
            boxes.id, 
            boxes.cls
            ):

            x1, y1, x2, y2 = box
            current_id = int(id)
            class_id = int(cls)
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            if class_id == 0:
                object_type = "person"
                person_count += 1

            elif class_id == 2:
                object_type = "car"
                car_count += 1

            else:
                object_type = "other"

            if current_id in previous_positions:
                prev_y = previous_positions[current_id]
                if (
                    prev_y < LINE_Y
                    and center_y >= LINE_Y
                    and current_id not in counted_ids
                ):
                    total_count += 1
                    counted_ids.add(current_id)
                    print(
                        f"passed!{int(current_id)},"
                        f"Total:{total_count}"
                    )
                    with open(csv_file, "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), 
                            current_id, 
                            object_type
                        ])
            previous_positions[current_id] = center_y
        annotated_frame = results[0].plot()
        cv2.line(
            annotated_frame,
            (0, 400),
            (frame.shape[1], 400),
            (0, 0, 255),
            3
        )
        cv2.putText(
            annotated_frame,
            f"Persons: {person_count}",
            (20, 40),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.putText(
            annotated_frame,
            f"Cars: {car_count}",
            (20, 80),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 100),
            2
        )
        cv2.putText(
            annotated_frame,
            f"TotalCount: {total_count}",
            (20, 120),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.imshow("Detection", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

df = pd.read_csv(csv_file)
df["timestamp"] = pd.to_datetime(
    df["timestamp"], 
    format="%Y-%m-%d-%H:%M:%S"
)

hourly_counts = (
    df.groupby(
        df["timestamp"].dt.hour, 
    )
    .size()
)
print(hourly_counts)

cap.release()
cv2.destroyAllWindows()