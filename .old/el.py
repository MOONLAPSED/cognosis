from typing import List, Union, TypeVar
import struct
import sys
import io
from abc import abstractmethod, ABC

T = TypeVar('T')

class ByteSerializer:
    @staticmethod
    def serialize(data: Union[str, bytes]) -> bytes:
        """Serialize data to bytes."""
        if isinstance(data, str):
            return data.encode()
        return data

    @staticmethod
    def deserialize(data: bytes) -> str:
        """Deserialize bytes to a string."""
        return data.decode()

class EmbeddingSerializer:
    @staticmethod
    def serialize(embedding: List[float], file_path: str) -> None:
        """Serialize an embedding (list of floats) to a binary file."""
        with open(file_path, "wb") as f:
            for value in embedding:
                f.write(struct.pack("f", value))

    @staticmethod
    def deserialize(file_path: str) -> List[float]:
        """Deserialize an embedding from a binary file into a list of floats."""
        embedding = []
        with open(file_path, "rb") as f:
            while True:
                data = f.read(4)  # Read 4 bytes at a time (for float)
                if not data:
                    break
                value = struct.unpack("f", data)[0]
                embedding.append(value)
        return embedding

class Atom(ABC):
    """Base class for atomic units."""
    @abstractmethod
    def __repr__(self):
        """Return a canonical representation of the atomic unit."""
        pass

class ByteStream(Atom):
    """Class representing a byte stream."""
    def __init__(self):
        self.stream = io.BytesIO()

    def __repr__(self):
        return f"ByteStream({self.stream.getvalue()})"

class STDIO(Atom):
    """Class representing standard input/output."""
    def __init__(self):
        pass

    def __repr__(self):
        return f"STDIN: {sys.stdin}, STDOUT: {sys.stdout}, STDERR: {sys.stderr}"

class BitField(Atom):
    """Atomic unit representing a bit field."""

    def __init__(self, value: int, length: int):
        self.value = value
        self.length = length

    def __and__(self, other: Union["BitField", int]) -> "BitField":
        """Bitwise AND operation."""
        if isinstance(other, BitField):
            value = self.value & other.value
            length = max(self.length, other.length)
        else:
            value = self.value & other
            length = self.length
        return BitField(value, length)

    def __or__(self, other: Union["BitField", int]) -> "BitField":
        """Bitwise OR operation."""
        if isinstance(other, BitField):
            value = self.value | other.value
            length = max(self.length, other.length)
        else:
            value = self.value | other
            length = self.length
        return BitField(value, length)

    def __repr__(self):
        """Return a canonical representation of the bit field."""
        return f"{self.value:0>{self.length}b}"


# Internet Protocol Stack-Frames
class EthernetFrame:
    def __init__(self, source_mac: str, dest_mac: str, payload: T):
        self.source_mac = source_mac
        self.dest_mac = dest_mac
        self.payload = payload

    def generate_frame(self) -> bytes:
        """Generate Ethernet frame."""
        # Implementation specific to Ethernet frame format
        pass

    @classmethod
    def parse_frame(cls, frame_data: bytes) -> 'EthernetFrame':
        """Parse Ethernet frame."""
        # Implementation specific to Ethernet frame format
        pass

    def display(self) -> str:
        """Display Ethernet frame."""
        return f"Ethernet Frame: Source MAC - {self.source_mac}, Destination MAC - {self.dest_mac}"

    def __repr__(self):
        return f"EthernetFrame(source_mac={self.source_mac}, dest_mac={self.dest_mac}, payload={self.payload})"

class IPv6Header:
    def __init__(self, version: int, traffic_class: int, flow_label: int, payload_length: int, next_header: int, hop_limit: int,
                 source_address: str, destination_address: str, extension_headers: List[int] = None, payload: T = None):
        self.version = version
        self.traffic_class = traffic_class
        self.flow_label = flow_label
        self.payload_length = payload_length
        self.next_header = next_header
        self.hop_limit = hop_limit
        self.source_address = source_address
        self.destination_address = destination_address
        self.extension_headers = extension_headers if extension_headers else []
        self.payload = payload

    def __repr__(self):
        header_repr = (
            f"IPv6 Header\n"
            f"Version: {self.version}\n"
            f"Traffic Class: {self.traffic_class}\n"
            f"Flow Label: {self.flow_label}\n"
            f"Payload Length: {self.payload_length}\n"
            f"Next Header: {self.next_header}\n"
            f"Hop Limit: {self.hop_limit}\n"
            f"Source Address: {self.source_address}\n"
            f"Destination Address: {self.destination_address}\n"
        )

        if self.extension_headers:
            header_repr += "Extension Headers: " + ", ".join(str(ext_header) for ext_header in self.extension_headers) + "\n"

        ascii_repr = (
            "  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n"
            " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
            f" |Version| Traffic Class |           Flow Label                  |\n"
            " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
            f" |         Payload Length        |  Next Header  |   Hop Limit   |\n"
            " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
            f" |                                                               |\n"
            f" +                                                               +\n"
            f" |                                                               |\n"
            f" +                      {self.source_address:<38}  +\n"
            f" |                                                               |\n"
            f" +                                                               +\n"
            f" |                                                               |\n"
            " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
            f" |                                                               |\n"
            f" +                                                               +\n"
            f" |                                                               |\n"
            f" +                      {self.destination_address:<38}  +\n"
            f" |                                                               |\n"
            f" +                                                               +\n"
            f" |                                                               |\n"
            " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
        )

        if self.extension_headers:
            ascii_repr += " |                   Extension Headers (if present)              |\n"
            ascii_repr += " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"

        return header_repr + '\n' + ascii_repr


class TCPSegment:
    def __init__(self, source_port: int, dest_port: int, seq_num: int, ack_num: int, data_offset: int, reserved: int, flags: int,
                 window_size: int, checksum: int, urgent_pointer: int, payload: T):
        self.source_port = source_port
        self.dest_port = dest_port
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.data_offset = data_offset
        self.reserved = reserved
        self.flags = flags
        self.window_size = window_size
        self.checksum = checksum
        self.urgent_pointer = urgent_pointer
        self.payload = payload

    def __repr__(self):
        return (f"TCPSegment(source_port={self.source_port}, dest_port={self.dest_port}, "
                f"seq_num={self.seq_num}, ack_num={self.ack_num}, "
                f"data_offset={self.data_offset}, reserved={self.reserved}, "
                f"flags={self.flags}, window_size={self.window_size}, "
                f"checksum={self.checksum}, urgent_pointer={self.urgent_pointer}, "
                f"payload={self.payload})")


class HTTPRequest:
    def __init__(self, method: str, uri: str, headers: dict, body: bytes):
        self.method = method
        self.uri = uri
        self.headers = headers
        self.body = body

    def __repr__(self):
        return (f"HTTPRequest(method='{self.method}', uri='{self.uri}', "
                f"headers={self.headers}, body={self.body})")


def main():
    # Example usage of classes
    byte_stream = ByteStream()
    print("Byte Stream:", byte_stream)

    stdio = STDIO()
    print("STDIO:", stdio)

    bit_field = BitField(10, 8)
    print("Bit Field:", bit_field)

    # Example serialization and deserialization
    data_to_serialize = "Hello, world!"
    serialized_data = ByteSerializer.serialize(data_to_serialize)
    print("Serialized Data:", serialized_data)
    
    deserialized_data = ByteSerializer.deserialize(serialized_data)
    print("Deserialized Data:", deserialized_data)

    # Example embedding serialization and deserialization
    embedding = [1.0, 2.0, 3.0]
    embedding_file = "embedding.bin"
    EmbeddingSerializer.serialize(embedding, embedding_file)
    deserialized_embedding = EmbeddingSerializer.deserialize(embedding_file)
    print("Deserialized Embedding:", deserialized_embedding)

    # Example usage of EthernetFrame
    ethernet_frame = EthernetFrame("00:11:22:33:44:55", "AA:BB:CC:DD:EE:FF", "Payload data")
    print("Ethernet Frame:", ethernet_frame)
    print("Generated Frame:", ethernet_frame.generate_frame())
    print("Parsed Frame:", EthernetFrame.parse_frame(b""))

    # Example usage of IPv6Header
    ipv6_header = IPv6Header(
        version=6,
        traffic_class=0,
        flow_label=123,
        payload_length=100,
        next_header=17,
        hop_limit=64,
        source_address="2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        destination_address="2001:0db8:85a3:0000:0000:8a2e:0370:7335",
        extension_headers=[],
        payload=None
    )
    print("IPv6 Header:", ipv6_header)

    # Example usage of TCPSegment
    tcp_segment = TCPSegment(
        source_port=1234,
        dest_port=5678,
        seq_num=1000,
        ack_num=2000,
        data_offset=5,
        reserved=0,
        flags=2,
        window_size=100,
        checksum=12345,
        urgent_pointer=0,
        payload=b"TCP Payload"
    )
    print("TCP Segment:", tcp_segment)

    # Example usage of HTTPRequest
    http_request = HTTPRequest(
        method="GET",
        uri="/index.html",
        headers={"Content-Type": "text/html"},
        body=b"HTTP Request Body"
    )
    print("HTTP Request:", http_request)

