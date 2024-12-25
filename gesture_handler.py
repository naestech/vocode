import numpy as np
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Gesture:
    name: str
    midiCommand: int
    midiValue: int

class GestureHandler:
    def __init__(self):
        # Define gesture thresholds and MIDI mappings
        self.gestures = {
            'index_up': Gesture('index_up', 0x90, 60),  # Note On, middle C
            'open_palm': Gesture('open_palm', 0xB0, 1),  # Control Change
            # Add more gestures as needed
        }
        self.previousGesture = None

    def processLandmarks(self, landmarks) -> Optional[Gesture]:
        # Convert landmarks to numpy array for easier processing
        points = np.array([[l.x, l.y, l.z] for l in landmarks.landmark])
        
        # Detect gestures based on landmark positions
        if self._isIndexUp(points):
            return self._handleGestureTransition('index_up')
        elif self._isOpenPalm(points):
            return self._handleGestureTransition('open_palm')
        
        self.previousGesture = None
        return None

    def _isIndexUp(self, points) -> bool:
        # Check if index finger is extended while others are closed
        # This is a simplified check - will be improved
        indexTip = points[8][1]  # Y coordinate of index fingertip
        indexBase = points[5][1]  # Y coordinate of index base
        return indexTip < indexBase

    def _isOpenPalm(self, points) -> bool:
        # Basic check for open palm gesture
        # Will be improved with proper finger tracking
        fingerTips = [points[i][1] for i in [8, 12, 16, 20]]  # Y coordinates of fingertips
        palmBase = points[0][1]  # Y coordinate of palm base
        return all(tip < palmBase for tip in fingerTips)

    def _handleGestureTransition(self, gestureName: str) -> Optional[Gesture]:
        gesture = self.gestures.get(gestureName)
        if gesture and gesture != self.previousGesture:
            self.previousGesture = gesture
            return gesture
        return None 