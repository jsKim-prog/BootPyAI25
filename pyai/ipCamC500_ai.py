# 선행준비 : ip 카메라를 준비한다.
# ip 카메라의 제조회사에 가서 관련 네트워크 설정을 마무리 한다.
# 제조회사의 vms 프로그램을 설치한다.(ip와 암호, rtsp 프로토콜 활성화)

# 파이썬과 프론트를 연동하는 mqtt api를 활용한다.
# mqtt : 실시간 출력 프로토콜 https://underflow101.tistory.com/22
# mqtt 브로커용 프로그램 모스키토 api를 활용한다.
# https://mosquitto.org/download/ 버전을 맞추는 것이 중요! - mosquitto 2.0.18

# 모스키토 환경설정 변경 C:\Program Files\mosquitto\mosquitto.conf (관리자권한 열기)
# MQTT 기본 리스너 설정
# listnet 1883
# protocol mqtt
#
# # WebSocket 리스너 설정
# listner 9001
# protocol websockets
#
# #익명의 접속 허용
# allow_anonymous true

# 방화벽 설정 추가 -> 실행 -> wf.msc 1883, 9001 열기
# cmd 터미널에서 환경설정 적용 실행 : mosquitto -c mosquitto.conf -v
# cmd 실행해 두어야 함
# 만약 안되면 services.msc에 가서 서비스 재실행

import base64
import io
from PIL import Image
import numpy as np
import json
from ultralytics import YOLO
import paho.mqtt.client as mqtt  # 브로커 추가
import cv2
import time

model = YOLO('yolov8n.pt')
client = mqtt.Client()  # mosquitto -c mosquitto.conf
topic = '/camera/objects'  # 경로
client.connect('localhost', 1883, 60)


# 연결용 함수
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


# 객체감지용 색상 함수
def get_colors(num_colors):
    np.random.seed(0)
    colors = [tuple(np.random.randint(0, 255, 3).tolist()) for _ in range(num_colors)]
    return colors


class_names = model.names  # 모델에서 받은 클래스 이름
num_classes = len(class_names)  # 클래스 번호
colors = get_colors(num_classes)  # 사각박스 컬러색

client.on_connect = on_connect  # 클라이언트 연결정보
cap = cv2.VideoCapture('rtsp://admin:mbc312AI!!@192.168.0.8:554/taem1')  # rtsp 정보(vms 참고)
# https://deep-learning-study.tistory.com/107
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#cap.set(cv2.CAP_PROP_FPS, 24)


# bRsec = False
# prevTime =0

##############전처리#################################

# 모델이 객체를 탐지용 함수
def detect_objects(image: np.array):
    results = model(image, verbose=False)
    class_names = model.names

    for result in results:
        boxes = result.boxes.xyxy
        confidences = result.boxes.conf
        class_ids = result.boxes.cls
        for box, confidences, class_ids in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)
            label = class_names[int(class_ids)]
            cv2.rectangle(image, (x1, y1), (x2, y2), colors[int(class_ids)], 2)
            cv2.putText(image, f'{label} {confidences:.2f}', (x1, y1),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, colors[int(class_ids)], 2)
    return image


# 객체탐지 반복용 루프
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    result_image = detect_objects(frame)

    _, buffer = cv2.imencode('.jpg', result_image)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')

    payload = json.dumps({'image': jpg_as_text})
    client.publish(topic, payload)
    #cv2.imshow('Frame', result_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # 영상 출력 중에 q가 입력되면 종료
        break
cap.release()  # VideoCapture
cv2.destroyAllWindows()  # 창닫기
client.disconnect()  # 연결해제
