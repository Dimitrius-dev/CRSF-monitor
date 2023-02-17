from serial import Serial

from config import timeout, baudrate, port


class SerialReader():
    def __init__(self):
        self.__ser = Serial(timeout=timeout)
        self.__ser.baudrate = baudrate
        self.__ser.port = port
        self.__ser.open()
        print("started")

    # output binary list of channels
    def get_channels(self, b: bytes) -> list[str]:
        text = ""
        for i in b:
            text += str(bin(i)).replace("0b", "").rjust(8, '0')

        chunk_size = 11
        chunks = [text[i:i + 11] for i in range(0, len(text), 11)]

        return chunks

    def parse(self) -> list[str]:
        while True:
            while True:
                fir_byte = int.from_bytes(self.__ser.read(), byteorder='big')
                if fir_byte == 200:
                    break
            print("msg start")

            msg_size_sec_byte = int.from_bytes(self.__ser.read(), byteorder='big')
            print("size", msg_size_sec_byte)
            if msg_size_sec_byte != 24:
                continue

            msg_type_sec_byte = int.from_bytes(self.__ser.read(), byteorder='big')
            print("type", msg_type_sec_byte)
            if msg_type_sec_byte != 22:
                continue

            size_of_sys_info = 2
            msg = self.__ser.read(msg_size_sec_byte - size_of_sys_info)
            # print("msg:\n", msg)

            return self.get_channels(msg)