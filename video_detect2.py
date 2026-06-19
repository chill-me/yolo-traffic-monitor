from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results =  model.predict(
    source="6387-191695740_medium.mp4",
    save=True
)

print("done!!!")

