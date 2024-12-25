# Vocode - Gesture-Based MIDI Controller

A real-time hand gesture recognition system that converts hand movements into MIDI signals for controlling digital audio workstations.
Inpsired by [julip.mp3](https://www.tiktok.com/@julip.mp3/video/7446504594135321902)

## Features
- Real-time hand tracking using webcam
- Gesture-to-MIDI signal conversion
- Visual feedback for detected gestures
- Virtual MIDI port support
- Debug view for monitoring gesture states

## Tech Stack
- Python 3.8+
- MediaPipe (hand tracking)
- Mido (MIDI communication)
- OpenCV (video capture)
- NumPy (calculations)
- python-rtmidi

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Ensure your webcam is connected and accessible.
3. Run the program:
```bash
python main.py
```
4. To exit the program, press 'q'.

## Development Status
Currently in early development with basic MIDI functionality and hand tracking implementation. Next phase will focus on integrating with a software synthesizer for sound output.

## Requirements
- Webcam
- Python 3.8 or higher
- Compatible DAW for MIDI input (coming soon)