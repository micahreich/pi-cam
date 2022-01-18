import bluetooth


class BluetoothHost:
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        self.port = self.server_sock.getsockname()[1]

        # Generated this on David's laptop
        self.uuid = "37D28FE7-A26C-41C9-AE22-3501D9E47DAA"

        bluetooth.advertise_service(self.server_sock, self.name,
                                    service_id=self.uuid, service_classes=[
                                        self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])

        print("Waiting for connection on RFCOMM channel", self.port)

        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from", self.client_info)
        self.listen()
        pass

    def listen(self):
        try:
            while True:
                data = self.client_sock.recv(1024)
                if not data:
                    break
                print("Received", data)
                self.callback(data)
        except OSError:
            pass


def display_info(data):
    # Display the info here
    print(data)


host = BluetoothHost("PI-CAM-AEPI", display_info)
