# pip install pybluez
import bluetooth

uuid = "37D28FE7-A26C-41C9-AE22-3501D9E47DAA"


class BluetoothClient:
    def __init__(self, name):
        self.name = name
        self.connected = False
        pass

    def connect(self):
        print("Performing scan...")
        nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True,
                                                    flush_cache=True, lookup_class=False)
        for addr, name in nearby_devices:
            if name == self.name:
                self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                service_matches = bluetooth.find_service(
                    uuid=uuid, address=addr)

                self.sock.connect(
                    (service_matches[0]["host"], service_matches[0]["port"]))
                self.connected = True
                print("Connected.")
                return
        print("No device found.")
        return

    def send_info(self, data):
        self.sock.send(data)
        return


client = BluetoothClient("PI-CAM-AEPI")
client.connect()
