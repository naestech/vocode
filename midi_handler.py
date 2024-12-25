import rtmidi
import logging

logger = logging.getLogger(__name__)

class MidiHandler:
    def __init__(self):
        self.midi_out = rtmidi.MidiOut()
        self.available_ports = self.midi_out.get_ports()
        self.port_open = False
        
    def list_ports(self):
        """Show available MIDI ports"""
        if not self.available_ports:
            logger.warning("No MIDI ports available. Please check if IAC Driver is enabled.")
            logger.info("To enable IAC Driver: Open Audio MIDI Setup > Window > Show MIDI Studio > IAC Driver > Device is online")
        else:
            print("\nAvailable MIDI ports:")
            for i, port in enumerate(self.available_ports):
                print(f"Port {i}: {port}")
    
    def connect_to_port(self, port_number):
        """Connect to a specific MIDI port"""
        try:
            if 0 <= port_number < len(self.available_ports):
                self.midi_out.open_port(port_number)
                self.port_open = True
                logger.info(f"Connected to MIDI port: {self.available_ports[port_number]}")
                return True
            else:
                logger.error("Invalid port number")
                return False
        except Exception as e:
            logger.error(f"Failed to connect to MIDI port: {e}")
            return False
    
    def send_note(self, note, velocity=64, channel=0):
        """Send MIDI note (0-127)"""
        try:
            if self.port_open:
                # Note on
                note_on = [0x90 + channel, note, velocity]
                self.midi_out.send_message(note_on)
                logger.debug(f"Sent MIDI note: {note}")
                
                # Note off (after a short duration)
                note_off = [0x80 + channel, note, 0]
                self.midi_out.send_message(note_off)
        except Exception as e:
            logger.error(f"Failed to send MIDI note: {e}")
    
    def close(self):
        """Clean up MIDI resources"""
        if self.port_open:
            self.midi_out.close_port()
            self.port_open = False 