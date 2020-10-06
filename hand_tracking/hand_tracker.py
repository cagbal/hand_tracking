import csv
import math

import cv2
import numpy as np
from shapely.geometry import Polygon

from filterpy.kalman import KalmanFilter

from hand_tracking.utils import count_None



class HandTracker():
    """
    Incredibly simple Tracking
    
    Calculating only a simple score by using a previous
    detections  
    """
    def __init__(self, 
      memory_capacity: float, 
      iou_threshold: float):

        self._memory_capacity = memory_capacity
        
        self._memory = []

        self._iou_threshold = iou_threshold

        self._path_and_id = []

        self._current_id = 0

        self._path = []

        self._kf = KalmanFilter(dim_x=8, dim_z=1)

        self._kf.x = np.array([2., 0.])

    def push_memory(self, bbox: np.array):
        self._memory.append(bbox)

        if len(self._memory) > self._memory_capacity:
            self._memory.pop(0)

    def track(self):

        none_occurences = count_None(self._memory)

        if none_occurences == self._memory_capacity:
            path_and_id = self._path, self._current_id
            self._current_id +=1
            self._memory = []
            self._path = []
            return path_and_id
        else:
            return None

        
        
 
    @staticmethod
    def euclidean(pt1: tuple, pt2: tuple):
        return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)
    
    @staticmethod
    def mean_point(list_of_pts: list):
        x = 0
        y = 0

        for pt in list_of_pts:
            x += pt[0]
            y += pt[1]

        x, y = x/len(list_of_pts), y/len(list_of_pts)

        return x, y

    @staticmethod
    def calculate_iou(bbox1: Polygon, bbox2: Polygon):
        #iou for rotated rectangles
        iou = bbox1.intersection(bbox2).area / \
            bbox1.union(bbox2).area

        return iou

    def filter(self):
        # means there is no valid detection
        if self._memory is None or self._memory[-1] is None:
            return None
        
        # search backwards until finding a not None value
        idx_non_none = -1
        for i in range(len(self._memory)-2, -1, -1):
            if self._memory[i] is not None:
                idx_non_none = i
                break    
        # not found
        if idx_non_none < 0:
            return None
        
        mu_incoming = self.mean_point(self._memory[-1])

        last_bbox = Polygon(self._memory[idx_non_none])
        incoming_bbox = Polygon(self._memory[-1])
        
        iou = self.calculate_iou(last_bbox, incoming_bbox)

        print(iou)

        if iou > self._iou_threshold:
            self._path.append(mu_incoming)
            #self._memory[-1] = None
        else:
            self._memory[-1] = None
            #self._path.append(mu_incoming)

    def __call__(self, bbox: list):
        self.push_memory(bbox)
        self.filter()
        path_and_id = self.track()

        return path_and_id
        
        
        
