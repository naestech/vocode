from midi_handler import MidiHandler
import time
import logging

logging.basicConfig(level=logging.INFO)

def test_midi():
    midi = MidiHandler()
    
    print("\n=== MIDI Port Test ===")
    midi.list_ports()
    
    port_num = int(input("\nChoose a port number (or -1 to exit): "))
    if port_num >= 0 and midi.connect_to_port(port_num):
        print("\nPlaying test notes... (Press Ctrl+C to stop)")
        try:
            while True:
                print("Playing C major chord")
                for note in [60, 64, 67]:  # C major chord
                    midi.send_note(note)
                    time.sleep(0.2)
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nTest complete!")
    
    midi.close()

if __name__ == "__main__":
    test_midi() 