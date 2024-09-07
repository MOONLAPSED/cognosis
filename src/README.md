# AtomicBot Standard Specification

## Table of Contents

- [AtomicBot Standard Specification](#atomicbot-standard-specification)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Scope](#2-scope)
  - [3. Normative References](#3-normative-references)
  - [4. Definitions](#4-definitions)
  - [5. Events](#5-events)
    - [Event Format](#event-format)
  - [6. Actions](#6-actions)
    - [6.1 Sending a Message Example](#61-sending-a-message-example)
  - [7. HTTP Communication](#7-http-communication)
    - [7.1 Configuration](#71-configuration)
    - [7.2 Authentication](#72-authentication)
    - [7.3 Content Types](#73-content-types)
    - [7.4 Event Polling](#74-event-polling)
  - [7.5 Webhook](#75-webhook)
      - [7.5.1 Webhook Headers](#751-webhook-headers)
      - [7.5.2 Webhook Authentication](#752-webhook-authentication)
      - [7.5.3 Webhook Timeout](#753-webhook-timeout)
  - [8. WebSocket Communication](#8-websocket-communication)
    - [8.1 Authentication](#81-authentication)
    - [8.2 Events and Actions](#82-events-and-actions)
    - [8.3 WebSocket Forward](#83-websocket-forward)
    - [8.4 WebSocket Reverse](#84-websocket-reverse)
  - [9. Data Types](#9-data-types)
    - [9.1 Type Values](#91-type-values)
    - [9.2 Action Response](#92-action-response)
    - [9.3 Event Format](#93-event-format)
    - [9.4 Action Request Format](#94-action-request-format)
    - [9.5 Action Response Format](#95-action-response-format)
  - [10. Return Codes](#10-return-codes)
    - [10.1 Request Errors](#101-request-errors)
    - [10.2 Handler Errors](#102-handler-errors)
  - [11. Robot Self Identification](#11-robot-self-identification)
  - [12. Security Considerations](#12-security-considerations)
    - [12.1 Heuristics](#121-heuristics)
  - [13. Compliance and Conformance](#13-compliance-and-conformance)
  - [14. Examples and Use Cases](#14-examples-and-use-cases)
    - [14.1 Sending a Message Example](#141-sending-a-message-example)
    - [14.2 Receiving an Event Example](#142-receiving-an-event-example)
  - [15. Markdown Encoding and Double-Bracketed Entities](#15-markdown-encoding-and-double-bracketed-entities)

## 1. Introduction

The AtomicBot standard defines a common API for developing chatbots, standardizing communication, data formats, and interfaces. It aims to provide interoperability between different chatbot platforms and implementations.

## 2. Scope

This document specifies the communication protocols, data formats, and interfaces for implementing and using AtomicBot. It covers the structure of events, action requests, and responses, as well as supported communication methods.

## 3. Normative References

* [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt): Key words for use in RFCs to Indicate Requirement Levels
* JSON Data Interchange Format - ECMA-404

## 4. Definitions

| Term                     | Definition                                           |
| ------------------------ | ---------------------------------------------------- |
| Robot/Bot                | chatbot that processes inputs and generates responses|
| User                     | Person using the chatbot                             |
| Inference                | process of user input to generate response           |
| Inference point          | Platforms like OpenAI or Ollama provide chatbot APIs |
| AtomicBot                | The AtomicBot API specification or an instance of one|

## 5. Events

### Event Format

[[Events]] are objects with required fields:

- `id`: Unique ID of the event
- `type`: The type of event, such as a message or a reaction
- `detail_type`: Optional subtype or detail defining the event context (e.g., private, group, or channel)
- `message`: The content of the event (e.g., text, image, file)
- `time`: The timestamp of the event

Additional optional fields:

* (Optional)`source`: The origin of the event, such as a user, group, or channel
* (Optional)`target`: The intended recipient or target of the event
* (Optional)`content`: The main content, including text, image, or file associated with the event
* (Optional)`metadata`: Additional metadata to provide more context about the event, such as file size, image resolution, etc.

```json
{
  "id": "123",
  "type": "message",
  "detail_type": "private",
  "message": [
    {"type": "text", "data": {
      "text": "Hello world"
    }}
  ]
}
```

## 6. Actions

[[Action requests]] are sent by the application to request services. [[Responses]] are returned by [[AtomicBot]] after processing the requests.

### 6.1 Sending a Message Example

Action Request Example:

```json
{
  "action": "send_message",
  "params": {
    "message": ["Hi there!"]
  },
  "self": {
    "platform": "telegram",
    "user_id": "123"
  }
}
```

Action Response Example:

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "result": "success"
  },
  "echo": "123"
}
```

## 7. HTTP Communication

### 7.1 Configuration

[[AtomicBot]] runs an HTTP server based on configuration:

- `host`: Listening IP
- `port`: Listening port
- `access_token`: Authentication token
- `event_enabled`: Enable event polling
- `event_buffer_size`: Event buffer size
- `ssl_cert_path`: Path to the SSL certificate file for HTTPS connections
- `ssl_key_path`: Path to the SSL private key file for HTTPS connections


[[AtomicBot]] handles requests at `/` and returns action responses.

### 7.2 Authentication

If `access_token` is set, [[AtomicBot]] authenticates via:

- Authorization header
- access_token query parameter

### 7.3 Content Types

Supported request content types:

- `application/json` (MUST be supported)
- `application/msgpack` (MAY be supported)

Response Content-Type mirrors request.

### 7.4 Event Polling

If `event_enabled` is true, [[AtomicBot]] supports `get_latest_events` to poll events. It provides an event buffer of configurable `event_buffer_size`.

## 7.5 Webhook

[[AtomicBot]] supports webhooks for pushing events to an external endpoint. Configuration for the webhook includes:

- `url`: The destination URL where events will be posted.
- `access_token`: Optional authentication token.
- `timeout`: The maximum duration before a webhook request times out.

#### 7.5.1 Webhook Headers

Required request headers:

- `Content-Type`: application/json
- `User-Agent`: AtomicBot version
- `X-AtomicBot-Version`: AtomicBot version
- `X-Impl`: AtomicBot implementation

Optional `Authorization` header for authentication.

#### 7.5.2 Webhook Authentication

[[AtomicBot]] allows multiple ways to authenticate webhook requests:

1. **Authorization Header**: Include the token in the `Authorization` HTTP header.
   
   Example: `Authorization: Bearer <access_token>`

2. **Query Parameter**: Alternatively, the `access_token` can be sent as a query parameter in the URL: `GET /webhook?access_token=<access_token>`

#### 7.5.3 Webhook Timeout

Request timeout is based on the configured timeout value.

## 8. WebSocket Communication

[[AtomicBot]] supports [[WebSocket]] server and client roles. It forwards events to clients and handles action requests.

### 8.1 Authentication

If `access_token` is set, [[AtomicBot]] authenticates before handshake via: `Authorization: Bearer <access_token>` header. Authentication is done by:

- Sending an `Authorization` header during the WebSocket handshake request:
- Alternatively, passing the `access_token` as a query parameter in the WebSocket URL: `ws://<host>:<port>?access_token=<access_token>`

### 8.2 Events and Actions

- Events as JSON
- Action requests as JSON or MessagePack
- Responses use the request format

### 8.3 WebSocket Forward

[[AtomicBot]] runs a WebSocket server based on configuration:

- `host`: Listening IP
- `port`: Listening port
- `access_token`: Authentication

It accepts connections at `/` and handles events and actions.

### 8.4 WebSocket Reverse

[[AtomicBot]] connects to a WebSocket endpoint based on configuration:

- `url`: WebSocket URL
- `access_token`: Authentication
- `reconnect_interval`: Reconnect interval

It handles events and actions after connecting.

## 9. Data Types

### 9.1 Type Values

[[AtomicBot]] supports the following data types for requests and responses:

- `Integer`: int64, uint64, int32, uint32, int16, uint16, int8, uint8
- `Float`: float64
- `String`: string
- `Bytes`: Base64-encoded string or byte array
- `Array`: array of any type (`any[]`)
- `Map`: map of key-value pairs (`map[key_type]value_type`)
- `Object`: map of string keys and any type values (`map[string]any`)
- `Timestamp`: ISO 8601 or Unix epoch format representing a specific point in time
- `Boolean`: True or False
- `Null`: `nil`, `undefined`, or `not a number`

### 9.2 Action Response

An [[Action response]] is an object with the following required fields:

- `resp`: Action name
- `status`: Status of the action (e.g., ok or failed)
- `retcode`: Return code
- `data`: Response data
- `message`: Optional error message, if any

### 9.3 Event Format

An [[Event]] is an object with the following required fields:

- `id`: Unique event ID
- `self`: Sender's identity
- `time`: Timestamp of the event (ISO 8601 or Unix epoch format)
- `type`: Type of event

### 9.4 Action Request Format

An [[Action request]] is an object with the following required fields:

- `action`: The action name
- `params`: Action-specific parameters

Optional fields:

- `echo`: Request identifier, echoed back in the response
- `self`: Sender's identity

### 9.5 Action Response Format

An [[Action response]] is an object with the following required fields:

- `status`: Status of the response (e.g., ok or failed)
- `retcode`: Return code
- `data`: Response data
- `message`: Optional error message, if applicable

Optional fields:

- `echo`: Mirrors the request identifier

## 10. Return Codes

Return codes are used to indicate the result of action requests and event processing. [[AtomicBot]] categorizes errors into three major types:

- `0`: Successful execution.
- `1xxxx`: Client-side request errors.
- `2xxxx`: Server-side handler errors.
- `3xxxx`: Execution errors (e.g., timeout, memory limit).

### 10.1 Request Errors

These errors indicate issues with the request, similar to HTTP 4xx client errors:

| Code   | Error                | Cause                       |
| ------ | -------------------- | --------------------------- |
| 10001  | Bad Request           | Malformed request format     |
| 10002  | Unsupported Action    | Action is not implemented    |
| 10003  | Bad Parameter         | Invalid parameters provided  |

### 10.2 Handler Errors

Similar to HTTP 5xx server errors.

| Code   | Error                  | Cause                             |
| ------ | ---------------------- | --------------------------------- |
| 20001  | Bad Handler            | Implementation error              |
| 20002  | Internal Handler Error | Uncaught exception                |
| 20003  | Timeout                | Request took too long to process  |
| 20004  | Memory Exhaustion      | Handler exceeded memory limits    |


## 11. Robot Self Identification

TODO: Add detailed description of robot self-identification fields and format.

## 12. Security Considerations

### 12.1 Heuristics
- Ensure secure transmission (e.g., TLS/SSL) for HTTP and WebSocket communication.
- Use strong authentication mechanisms to protect against unauthorized access.
- Validate and sanitize all input data to prevent injection attacks.

These practices are necessary to ensure the safety and integrity of [[AtomicBot]], especially in production environments.

"Production" refers to, at a minimum, any networking beyond the local dev-env. To secure the interaction between clients and [[AtomicBot]], the following security measures must be in place for networked environments:

- Encryption: Ensure secure transmission using TLS/SSL for both HTTP and WebSocket communication. Self-signed or third-party certificates should be properly configured for production environments.
- Authentication: Use strong authentication mechanisms like OAuth 2.0 or token-based authentication to restrict unauthorized access.
- Input Validation: All input data must be thoroughly validated and sanitized to prevent common injection attacks like SQL injection or cross-site scripting (XSS).
- Access Control: Implement role-based access control (RBAC) for different users and bots to ensure that only authorized entities can trigger certain actions or access sensitive data.
- Rate Limiting - To prevent denial-of-service (DoS) attacks, enforce rate-limiting for both HTTP and WebSocket endpoints.


## 13. Compliance and Conformance

To be compliant with the [[AtomicBot Standard]], implementations MUST adhere to the protocols and data formats specified in this document. Implementations SHOULD provide conformance tests to validate compliance.

## 14. Examples and Use Cases

### 14.1 Sending a Message Example

To send a message, the application sends an [[action request]]:

```json
{
  "action": "send_message",
  "params": {
    "message": ["Hi there!"]
  },
  "self": {
    "platform": "telegram",
    "user_id": "123"
  }
}
```

The [[AtomicBot]] responds:

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "result": "success"
  },
  "echo": "123"
}
```

### 14.2 Receiving an Event Example

An example [[event]] received from [[AtomicBot]]:

```json
{
  "id": "123",
  "time": 1632847927,
  "type": "message",
  "detail_type": "private",
  "sub_type": "",
  "self": {
    "platform": "telegram",
    "user_id": "123"  
  },
  "message": [
    {
      "type": "text",
      "data": {
        "text": "Hello world"
      }
    }
  ]
}
```

## 15. Markdown Encoding and Double-Bracketed Entities

```markdown
#Markdown Encoding and Linkage

This specification is designed to be readable in plain text and common markdown renderers, leveraging both double-bracketed entities and angle-bracketed chunks for enhanced interactivity and modularity.
Double-Bracketed Entities

To facilitate knowledge graphing and associative linking of concepts, significant entities are enclosed in double brackets like this: [[Entity Name]]. When rendered in environments that support it (such as Obsidian), the double-bracketed terms become clickable links that can display contextual information and connections to related concepts. These entities are associated with the ~/kb/* knowledge base directory.

For example:

    [[API]] could link to documentation on what an API is.
    [[Chatbot]] may link to background on chatbots.
    [[JSON Data Interchange Format]] could expand into details on the JSON specification.

This makes the document itself an interactive knowledge repository in supported environments, while still being readable as plain markdown elsewhere. The double-bracket syntax was chosen specifically for compatibility with the popular Obsidian.md format. Although not a requirement of the AtomicBot specification, using this markup style can turn documentation into a powerful conceptual knowledge base when authored with tools like Obsidian that support this notation.
Angle-Bracketed Chunks

To organize and modularize the document, this specification leverages the use of angle-bracketed chunks. Chunks are denoted by double angle brackets like this: <<chunk_name>>. This format allows for the inclusion of code or content sections from different parts of the document in a structured and readable way. These chunks are associated with the ~/db/* database section, and the system is designed to search this directory for any angle-bracketed entities and attempt to resolve them to specific file system objects.

When rendered or processed in the [[cognosis]] literate cognitive framing environment (CLI and runtime), the double angle-bracketed chunks act as placeholders for code or content blocks defined elsewhere in the document. Additionally, these chunks can be used as anchor tags, allowing for micro-navigation to specific subsections in a command line interface style. This enhances the document's usability by enabling quick navigation to key sections directly.

For instance:

    <<initialization>> could link to a file system object in ~/db/* that initializes variables or settings.
    <<function_definitions>> might navigate to a section compiling all function definitions together.
    <<cleanup>> could ensure resources are properly released at the end of a script.

This chunking approach makes it easier to navigate and understand the document's structure, especially in larger specifications or literate programs. The double angle-bracket syntax was chosen for its clarity and compatibility with many literate programming conventions, fitting seamlessly with tools that support this notation. While not a requirement of the AtomicBot specification, using this markup style can transform documentation into a modular and easily navigable structure, especially when used with tools that support angle-bracketed chunks and command line navigation.
```
