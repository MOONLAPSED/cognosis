"""
Value Encoding

The commands and headers are encoded in UTF-8. All frames except the CONNECT and CONNECTED frames will also escape any carriage return, line feed or colon found in the resulting UTF-8 encoded headers.

Escaping is needed to allow header keys and values to contain those frame header delimiting octets as values. The CONNECT and CONNECTED frames do not escape the carriage return, line feed or colon octets in order to remain backward compatible with STOMP 1.0.

C style string literal escapes are used to encode any carriage return, line feed or colon that are found within the UTF-8 encoded headers. When decoding frame headers, the following transformations MUST be applied:

    \r (octet 92 and 114) translates to carriage return (octet 13)
    \n (octet 92 and 110) translates to line feed (octet 10)
    \c (octet 92 and 99) translates to : (octet 58)
    \\ (octet 92 and 92) translates to \ (octet 92)

Undefined escape sequences such as \t (octet 92 and 116) MUST be treated as a fatal protocol error. Conversely when encoding frame headers, the reverse transformation MUST be applied.
"""