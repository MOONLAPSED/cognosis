
"""
STOMP
STOMP is a frame based protocol, with frames modelled on HTTP. A frame consists of a command, a set of optional headers and an optional body. STOMP is text based but also allows for the transmission of binary messages. The default encoding for STOMP is UTF-8, but it supports the specification of alternative encodings for message bodies.

Destinations
In STOMP, the concept of a "destination" is central to where messages are sent and from where they are received. A destination is a general term that can refer to different things depending on the message broker's implementation. For example, in some brokers, a destination might be a queue where messages are stored until a consumer retrieves them. In others, it might be a topic used for publish-subscribe messaging, where messages are immediately broadcast to all subscribed consumers.

Opaque Strings
STOMP treats destination identifiers as "opaque strings," meaning that the protocol doesn't assign any structure or inherent meaning to these strings. They are just sequences of characters that are meaningful to the server. For instance, one server could use a destination string like "/queue/orders" to represent a queue for order messages, while another server might have a different naming convention or hierarchy.

Server Implementation Specific Syntax
Because STOMP doesn't enforce any particular structure for destinations, each server can define its own syntax for them. This means that the format of the destination strings can vary widely from one STOMP server to another. For instance, one server might use a URL-like structure while another might use a filesystem-like path.

Delivery Semantics
Delivery semantics, or "message exchange" semantics, define the rules or behaviors associated with message delivery when using a destination. STOMP itself does not specify what these semantics should be. Therefore, it is up to each STOMP server to implement its own semantics for handling messages.

For example, some possible delivery semantics include:

Retaining messages in a queue until they are explicitly acknowledged by a consumer.
Broadcasting messages to all active subscribers of a topic.
Storing messages persistently so they can be retrieved later, even if the consumer is not currently connected.
Flexibility for Server Implementations
Because STOMP does not strictly define destination syntax and delivery semantics, STOMP servers have the flexibility to support a variety of behaviors. This flexibility allows STOMP to be used in creative and varied ways that suit the needs of different applications.

For example, a broker could implement a destination that behaves like a topic for some clients and like a queue for others. Or it might support more advanced scenarios like message prioritization, delayed delivery, or filtering based on content or headers.



"""