"""rfc2616_stomp_client.py
A STOMP client is a user-agent which can act in two (possibly simultaneous) modes:

    as a producer, sending messages to a destination on the server via a SEND frame

    as a consumer, sending a SUBSCRIBE frame for a given destination and receiving messages from the server as MESSAGE frames.
"""