import cv2
import mediapipe as mp
import logging
from gesture_handler import GestureHandler
import sys
from midi_handler import MidiHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Vocode:
    def __init__(self):
        # Initialize video capture
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            logger.error("Failed to open video capture")
            raise RuntimeError("Could not open video capture")

        # Initialize hand tracking
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.gestureHandler = GestureHandler()
        
        # Initialize MIDI
        self.midi = MidiHandler()
        self.midi.list_ports()
        
        # Let user choose MIDI port
        if not self.midi.available_ports:
            logger.warning("No MIDI ports found!")
        else:
            print("\nAvailable MIDI ports:")
            self.midi.list_ports()
            port_number = int(input("\nChoose MIDI port number (or -1 to skip): "))
            if port_number >= 0:
                self.midi.connect_to_port(port_number)

    def run(self):
        logger.info("Starting video capture loop")
        while True:
            success, frame = self.cap.read()
            if not success:
                logger.error("Failed to capture video frame")
                break

            # Convert frame to RGB for MediaPipe
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgbFrame)

            if results.multi_hand_landmarks:
                for handLandmarks in results.multi_hand_landmarks:
                    # Draw landmarks for visual feedback
                    self.mpDraw.draw_landmarks(
                        frame, 
                        handLandmarks, 
                        self.mpHands.HAND_CONNECTIONS
                    )
                    
                    # Process gestures and generate MIDI
                    gesture = self.gestureHandler.processLandmarks(handLandmarks)
                    if gesture:
                        self.handleMidiSignal(gesture)

            cv2.namedWindow("vocode !! ദ്ദി˃̶ ꇴ ˂̶)♪ ༘⋆", cv2.WINDOW_NORMAL)
            cv2.imshow("vocode !! ദ്ദി˃̶ ꇴ ˂̶)♪ ༘⋆", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Press 'q' to quit
                break

        self.cleanup()

    def handleMidiSignal(self, gesture):
        """Map gestures to MIDI signals"""
        # Example mapping - adjust based on your gesture definitions
        if gesture == "open_palm":
            self.midi.send_note(60)  # Middle C
        elif gesture == "closed_fist":
            self.midi.send_note(62)  # D
        elif gesture == "pointing":
            self.midi.send_note(64)  # E

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.midi.close()

if __name__ == "__main__":
    vocode = Vocode()
    vocode.run() 