from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model("bus.jpg")

for result in results:
    print(result.boxes)

for result in results:
    annotated = result.plot()
    result.save(filename="result.jpg")

print("保存完了!")
