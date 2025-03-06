import threading
import time
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

# CONFIGURATION
PORT = "/dev/ttyAMA0"  # Adjust based on your setup
BAUD_RATE = 9600
DESTINATION_ADDR = "0013A20042361B36"  # Address of Raspberry Pi 2's XBee

class XBeeWrapper:
    def __init__(self, port, baud_rate):
        self.device = XBeeDevice(port, baud_rate)
        self.lock = threading.Lock()
        
        try:
            self.device.open()
            self.device.set_parameter("AP", bytearray([1]))  # Set API Mode
            print("XBee initialized in API mode.")
        except Exception as e:
            print(f"Error initializing XBee: {e}")
            self.device.close()
    
    def send(self, data):
        """Send data to the remote XBee."""
        with self.lock:
            try:
                remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(DESTINATION_ADDR))
                self.device.send_data(remote_device, data)
                print(f"Sent: {data} to {DESTINATION_ADDR}")
            except Exception as e:
                print(f"Send Error: {e}")
    
    def receive(self):
        """Read incoming messages."""
        with self.lock:
            try:
                response = self.device.read_data()
                if response:
                    print(f"Received: {response.data.decode()} from {response.remote_device.get_64bit_addr()}")
                    return response.data
            except Exception as e:
                print(f"Receive Error: {e}")
    
    def close(self):
        """Close XBee connection safely."""
        self.device.close()
        print("XBee device closed.")

def receive_loop(xbee):
    """ Continuously listen for incoming messages """
    while True:
        xbee.receive()
        time.sleep(0.5)

def main():
    xbee = XBeeWrapper(PORT, BAUD_RATE)

    # Start a thread to listen for messages
    recv_thread = threading.Thread(target=receive_loop, args=(xbee,), daemon=True)
    recv_thread.start()

    try:
        while True:
            msg = input("Enter message to send: ")
            if msg.lower() == "exit":
                break
            xbee.send(msg)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        xbee.close()

if __name__ == "__main__":
    main()
