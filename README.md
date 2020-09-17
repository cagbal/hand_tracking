## Hand tracking
Fork of https://github.com/metalwhale/hand_tracking

### Installation
```
$ git clone https://github.com/cagbal/hand_tracking
$ cd hand_tracking
$ pip install opencv-python tensorflow==2.1.0
```

### Usage
```
$ python webcam_demo.py
```

### Credits
- All the logic: https://github.com/metalwhale/hand_tracking
- `palm_detection_without_custom_op.tflite`：[*mediapipe-models*]
- `hand_landmark.tflite`：[*mediapipe*]
- `anchors.csv`and`hand_tracker.py`：[*hand_tracking*]

[*mediapipe-models*]: https://github.com/junhwanjang/mediapipe-models/tree/master/palm_detection/mediapipe_models
[*mediapipe*]: https://github.com/google/mediapipe/tree/master/mediapipe/models
[*hand_tracking*]: https://github.com/wolterlw/hand_tracking
