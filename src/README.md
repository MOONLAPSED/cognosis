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
  - [Add optional fields commonly used in events](#add-optional-fields-commonly-used-in-events)
  - [6. Actions](#6-actions)
    - [6.1 Actions Overview](#61-actions-overview)
    - [6.2 Sending a Message Example](#62-sending-a-message-example)
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
| Robot/Bot                | Chatbot                                              |
| Robot Platform           | Platforms like QQ, WeChat that provide chatbot APIs  |
| AtomicBot                | The standard or an implementation                    |
| AtomicBot Standard       | The AtomicBot API specification                      |
| AtomicBot Implementation | A program implementing the AtomicBot standard        |
| AtomicBot Application    | A program using AtomicBot to implement chatbot logic |
| AtomicBot SDK            | Helper libraries for building AtomicBot apps         |
| AtomicBot Library        | Reusable code for AtomicBot implementations          |

## 5. Events

### Event Format

[[Events]] are objects with required fields:

- `id`: Unique ID
- `type`: Event type
- `detail_type`: Optional detail defining subtype of event (e.g., private, group, channel)
- `message`: Event message content (e.g., text, image, file)

## Add optional fields commonly used in events

* `source`: The source/origin of the event (e.g., user, group, channel)
* `target`: The target/destination of the event
* `content`: The main content of the event (e.g., message text, image, file)
* `metadata`: Additional metadata about the event

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

### 6.1 Actions Overview

[[Action requests]] are sent by the application to request services. [[Responses]] are returned by [[AtomicBot]] after processing the requests.

### 6.2 Sending a Message Example

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

### 7.5 Webhook

[[AtomicBot]] pushes events to a webhook URL based on configuration:

- `url`: Webhook URL
- `access_token`: Authentication
- `timeout`: Request timeout

#### 7.5.1 Webhook Headers

Required request headers:

- `Content-Type`: application/json
- `User-Agent`: AtomicBot version
- `X-AtomicBot-Version`: AtomicBot version
- `X-Impl`: AtomicBot implementation

Optional `Authorization` header for authentication.

#### 7.5.2 Webhook Authentication

Authenticates via:

- Authorization header
- access_token query parameter

#### 7.5.3 Webhook Timeout

Request timeout is based on the configured timeout value.

## 8. WebSocket Communication

[[AtomicBot]] supports [[WebSocket]] server and client roles. It forwards events to clients and handles action requests.

### 8.1 Authentication

If `access_token` is set, [[AtomicBot]] authenticates before handshake via:

- Authorization header
- access_token query parameter

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

- `Integer`: int64, uint64, int32, uint32, int16, uint16, int8, uint8
- `Float`: float64
- `String`: string
- `Bytes`: Base64-encoded string or byte array
- `Array`: any[]
- `Map`: map[key_type]value_type
- `Object`: object (map[string]any)

### 9.2 Action Response

[[Action responses]] are objects with required fields:

- `resp`: Action name
- `status`: Status
- `retcode`: Return code
- `data`: Response data
- `message`: Error message

### 9.3 Event Format

[[Events]] are objects with required fields:

- `id`: Unique ID
- `self`: Sender identity
- `time`: Timestamp
- `type`: Event type

### 9.4 Action Request Format

[[Action requests]] are objects with required fields:

- `action`: Action name
- `params`: Parameters

Optional fields:

- `echo`: Identifier
- `self`: Sender identity

### 9.5 Action Response Format

[[Action responses]] are objects with required fields

:

- `status`: ok or failed
- `retcode`: Return code
- `data`: Response data
- `message`: Error message

Optional fields:

- `echo`: Mirrors request identifier

## 10. Return Codes

Return codes indicate execution status:

- 0: Success
- 1xxxx: Request errors
- 2xxxx: Handler errors
- 3xxxx: Execution errors

### 10.1 Request Errors

Similar to HTTP 4xx client errors.

| Code   | Error                | Cause                |
| ------ | -------------------- | -------------------- |
| 10001  | Bad Request          | Malformed request    |
| 10002  | Unsupported Action   | Unimplemented action |
| 10003  | Bad Param            | Invalid parameter    |

### 10.2 Handler Errors

Similar to HTTP 5xx server errors.

| Code   | Error                | Cause                |
| ------ | -------------------- | -------------------- |
| 20001  | Bad Handler          | Implementation error |
| 20002  | Internal Handler Error | Uncaught exception |

## 11. Robot Self Identification

TODO: Add detailed description of robot self-identification fields and format.

## 12. Security Considerations

- Ensure secure transmission (e.g., TLS/SSL) for HTTP and WebSocket communication.
- Use strong authentication mechanisms to protect against unauthorized access.
- Validate and sanitize all input data to prevent injection attacks.

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

When rendered or processed in the [[abraxus]] literate cognitive framing environment (CLI), the double angle-bracketed chunks act as placeholders for code or content blocks defined elsewhere in the document. Additionally, these chunks can be used as anchor tags, allowing for micro-navigation to specific subsections in a command line interface style. This enhances the document's usability by enabling quick navigation to key sections directly.

For instance:

    <<initialization>> could link to a file system object in ~/db/* that initializes variables or settings.
    <<function_definitions>> might navigate to a section compiling all function definitions together.
    <<cleanup>> could ensure resources are properly released at the end of a script.

This chunking approach makes it easier to navigate and understand the document's structure, especially in larger specifications or literate programs. The double angle-bracket syntax was chosen for its clarity and compatibility with many literate programming conventions, fitting seamlessly with tools that support this notation. While not a requirement of the AtomicBot specification, using this markup style can transform documentation into a modular and easily navigable structure, especially when used with tools that support angle-bracketed chunks and command line navigation.
```
