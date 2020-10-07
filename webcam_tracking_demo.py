import cv2

from hand_tracking.hand_detector import HandDetector
from hand_tracking.hand_tracker import HandTracker
from fusion.fusion import Fusion
from hand_tracking.utils import create_json_message

from hand_tracking.utils import KafkaClient

import time

WINDOW = "Hand Tracking"
PALM_MODEL_PATH = "models/palm_detection_without_custom_op.tflite"
LANDMARK_MODEL_PATH = "models/hand_landmark.tflite"
ANCHORS_PATH = "models/anchors.csv"

POINT_COLOR = (0, 255, 0)
CONNECTION_COLOR = (255, 0, 0)
THICKNESS = 2
BBOX_COLOR = (255, 255, 0)

cv2.namedWindow(WINDOW)
capture = cv2.VideoCapture(2)

if capture.isOpened():
    hasFrame, frame = capture.read()
else:
    hasFrame = False

TOPIC_NAME = "pa4.event.inbound"

kafka = KafkaClient()

fusion = Fusion()

detector = HandDetector(
    PALM_MODEL_PATH,
    LANDMARK_MODEL_PATH,
    ANCHORS_PATH,
    box_shift=0.2,
    box_enlarge=1.0,
    hand_probability_threshold=0.8
)

tracker = HandTracker(
    memory_capacity = 10,
    iou_threshold = 0.8
)

while hasFrame:
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    points, bbox = detector(image, only_palm=False)

    path_and_id = tracker(bbox)

  
    if path_and_id:
        if path_and_id[0]:
            
            object_map =  \
                {
                "left": 
                    {
                        "object_type": "ültje",
                        "object_id" : "111111"
                    },
                "right": 
                    {
                        "object_type": "corny",
                        "object_id" : "000000"
                    }
                }
            print(type(object_map))

            fusion.update_observations(path_and_id)

            event_type, position, probabilty, object_id, object_type =\
                fusion.fuse(
                    object_map,
                    image.shape[0],
                    image.shape[1]
                )

            message = create_json_message(      
                event_type, 
                position,
                probabilty,
                object_id,
                object_type
                )

            print(message)
            
            kafka.publish(TOPIC_NAME, message)

    if points is not None:
        for point in bbox:
            x, y = point
            cv2.circle(frame, (int(x), int(y)), THICKNESS * 2, BBOX_COLOR, THICKNESS)
    cv2.imshow(WINDOW, frame)
    hasFrame, frame = capture.read()
    key = cv2.waitKey(1)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
