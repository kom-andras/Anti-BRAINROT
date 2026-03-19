import cv2
from ultralytics import YOLO
import math
import time
import serial

ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(5)

print("Loading model...")
model = YOLO('yolov8n.pt')

classNames = model.names

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

last_alert_time = 0
cooldown = 5

while True:
    success, img = cap.read()
    if not success:
        break

    current_time = time.time()
    results = model(img, stream=True, verbose=False)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass == "cell phone":
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                conf = math.ceil((box.conf[0] * 100)) / 100

                if conf > 0.5:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

                    cv2.putText(img, f'Phone! ({conf*100})', (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    #cv2.imwrite("asd.jpg", img)
                    
                    if current_time - last_alert_time > cooldown:
                        print(f"Brainrot detected! ({time.ctime()})")
                        ser.write(b'ON\n')
                        last_alert_time = current_time

    cv2.imshow('No phone', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()