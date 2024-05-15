from typing import List
import struct
from typing import TypeVar, List, Union

# This describes a system with a Python runtime that leverages a shell script to interact with the environment in a structured and semantically meaningful way, allowing for complex operations governed by simplified interfaces exposed to the Python layer.

# TypeVar for generic types
T = TypeVar('T')

# Bytes (Streams)
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

# Embeddings (Unix File System Objects)
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
            "   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n"
            " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
            f" |Version| Traffic Class |           Flow Label                  |\n"
            " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
            f" |         Payload Length        |  Next Header  |   Hop Limit   |\n"
            " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
            f" |                                                               |\n"
            f" +                                                               +\n"
            f" |                                                               |\n"
            f" +                      {self.source_address:<38}   +\n"
            f" |                                                               |\n"
            f" +                                                               +\n"
            f" |                                                               |\n"
            " +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
            f" |                                                               |\n"
            f" +                                                               +\n"
            f" |                                                               |\n"
            f" +                      {self.destination_address:<38}   +\n"
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

class HTTPRequest:
    def __init__(self, method: str, uri: str, headers: dict, body: bytes):
        self.method = method
        self.uri = uri
        self.headers = headers
        self.body = body


def main():
    header = IPv6Header(
        version=6,
        traffic_class=0,
        flow_label=0x12345,
        payload_length=64,
        next_header=6,  # TCP
        hop_limit=64,
        source_address="2001:db8::1",
        destination_address="2001:db8::2",
        extension_headers=[0, 1, 2]
    )
    print(repr(header))
    eth_frame = EthernetFrame("00:11:22:33:44:55", "66:77:88:99:AA:BB", "Payload data")
    eth_frame.generate_frame()
    eth_frame.display()
    print(eth_frame)

if __name__ == "__main__":
    main()