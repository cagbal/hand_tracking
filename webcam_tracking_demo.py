import cv2

from hand_tracking.hand_tracker import HandDetector

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


detector = HandDetector(
    PALM_MODEL_PATH,
    LANDMARK_MODEL_PATH,
    ANCHORS_PATH,
    box_shift=0.2,
    box_enlarge=1.0,
    hand_probability_threshold=0.8
)

while hasFrame:
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    points, bbox = detector(image, only_palm=False)
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
