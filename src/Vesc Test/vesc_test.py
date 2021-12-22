import serial
import time
from base import VESCMessage
import codec
from getters import GetVersion
import threading
from Vedder_BLDC_Commands import VedderCmd


serial_port = 'COM8'
s = None


class PackerBase(object):
    """
    Packing is the same for stated and stateless. Therefore its implemented in this base class.
    """
    @staticmethod
    def _pack(payload):
        """
        Packs a payload.
        :param payload: byte string of payload
        :return: byte string of packed packet
        """
        if payload == b'':
            raise InvalidPayload("Empty payload")
        # get header/footer tuples
        header = Header.generate(payload)
        footer = Footer.generate(payload)
        # serialize tuples
        header = struct.pack(Header.fmt(header.payload_index), *header)
        footer = struct.pack(Footer.fmt(), *footer)
        return header + payload + footer


def encode(msg):
    """
    Encodes a PyVESC message to a packet. This packet is a valid VESC packet and
    can be sent to a VESC via your serial port.

    :param msg: Message to be encoded. All fields must be initialized.
    :type msg: PyVESC message

    :return: The packet.
    :rtype: bytes
    """
    msg_payload = VESCMessage.pack(msg)
    packet = codec.frame(msg_payload)
    return packet


def encode_request(msg_cls):
    """
    Encodes a PyVESC message for requesting a getter message. This function
    should be called when you want to request a VESC to return a getter
    message.

    :param msg_cls: The message type which you are requesting.
    :type msg_cls: pyvesc.messages.getters.[requested getter]

    :return: The encoded PyVESC message which can be sent.
    :rtype: bytes
    """
    msg_payload = VESCMessage.pack(msg_cls, header_only=True)
    packet = codec.frame(msg_payload)
    return packet


def decode(buffer):
    """
    Decodes the next valid VESC message in a buffer.

    :param buffer: The buffer to attempt to parse from.
    :type buffer: bytes

    :return: PyVESC message, number of bytes consumed in the buffer. If nothing
             was parsed returns (None, 0).
    :rtype: `tuple`: (PyVESC message, int)
    """
    msg_payload, consumed = codec.unframe(buffer)
    if msg_payload:
        return VESCMessage.unpack(msg_payload), consumed
    else:
        return None, consumed


def write(s, data, num_read_bytes=None):
        """
        A write wrapper function implemented like this to try and make it easier to incorporate other communication
        methods than UART in the future.
        :param data: the byte string to be sent
        :param num_read_bytes: number of bytes to read for decoding response
        :return: decoded response from buffer
        """
        s.write(data)
        if num_read_bytes is not None:
            while s.in_waiting <= num_read_bytes:
                time.sleep(0.000001)  # add some delay just to help the CPU
            response, consumed = decode(s.read(s.in_waiting))
            return response


class Alive(metaclass=VESCMessage):
    """Heartbeat signal to keep VESC alive"""
    id = VedderCmd.COMM_ALIVE
    fields = []


# statically save this message because it does not need to be recalculated
alive_msg = encode(Alive())


# Alive thread
def _heartbeat_cmd_func():
    """
    Continuous function calling that keeps the motor alive
    """
    while not _stop_heartbeat.isSet():
        time.sleep(0.1)
        if s:
            write(s, data=alive_msg)

def start_heartbeat():
    """
    Starts a repetitive calling of the last set cmd to keep the motor alive.
    """
    heart_beat_thread.start()

def stop_heartbeat():
    """
    Stops the heartbeat thread and resets the last cmd function. THIS MUST BE CALLED BEFORE THE OBJECT GOES OUT OF
    SCOPE UNLESS WRAPPING IN A WITH STATEMENT (Assuming the heartbeat was started).
    """
    if heart_beat_thread.is_alive():
        _stop_heartbeat.set()
        heart_beat_thread.join()


heart_beat_thread = threading.Thread(target=_heartbeat_cmd_func)
_stop_heartbeat = threading.Event()


class SetDutyCycle(metaclass=VESCMessage):
    """ Set the duty cycle.

    :ivar duty_cycle: Value of duty cycle to be set (range [-1e5, 1e5]).
    """
    id = VedderCmd.COMM_SET_DUTY
    fields = [
        ('duty_cycle', 'i', 100000)
    ]


class SetRotorPositionMode(metaclass=VESCMessage):
     """Sets the rotor position feedback mode.

     It is reccomended to use the defined modes as below:
         * DISP_POS_OFF
         * DISP_POS_MODE_ENCODER
         * DISP_POS_MODE_PID_POS
         * DISP_POS_MODE_PID_POS_ERROR

     :ivar pos_mode: Value of the mode
     """

     DISP_POS_OFF = 0
     DISP_POS_MODE_ENCODER = 3
     DISP_POS_MODE_PID_POS = 4
     DISP_POS_MODE_PID_POS_ERROR = 5

     id = VedderCmd.COMM_SET_DETECT
     fields = [
         ('pos_mode', 'b')
     ]


# a function to show how to use the class with a with-statement
def run_motor_using_with():
    s = serial.Serial()
    s.port = serial_port
    s.baudrate = 115200
    s.timeout = 0.05
    
    try:
        s.open()
        print(f'Connected to {serial_port}')
    except:
        print(f'Failed to connect to {serial_port}')

    s.write(encode(SetRotorPositionMode(SetRotorPositionMode.DISP_POS_MODE_ENCODER)))

    start_heartbeat()

    msg = GetVersion()
    print(str(write(s, encode_request(msg), 16)))

    e = False
    while not e:
        i = input()
        if i == 'e':
            e = True
            stop_heartbeat()
            s.close()
        else:
            write(s, encode(SetDutyCycle(float(i))))
        


if __name__ == '__main__':
    run_motor_using_with()

