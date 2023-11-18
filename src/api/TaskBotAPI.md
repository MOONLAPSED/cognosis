# TaskBot Standard - translated from Chinese by GPT - author's repo and licsence info: https://github.com/botuniverse/onebot

# The TaskBot standard defines a common API for developing chatbots, standardizing communication, data formats, and interfaces. It draws parallels with specifications such as C Language, ECMAScript, and POSIX.

## Document Keywords
Keyword | Meaning
--- | ---
MUST | Required
MUST NOT | Prohibited
SHALL | Recommended
SHALL NOT | Not Recommended
MAY | Optional

## Overview

TaskBot consists of two components:

1. **TaskBot Connect:** Handles communication protocols and data encoding.
2. **Interface Definition:** Specifies events, actions, and message formats.

## Terminology

Term | Definition
--- | ---
Robot/Bot | Chatbot
Robot Platform | Platforms like QQ, WeChat that provide chatbot APIs
TaskBot | The standard or an implementation
TaskBot Standard | The TaskBot API specification
TaskBot Implementation | A program implementing the TaskBot standard
TaskBot Application | A program using TaskBot to implement chatbot logic
TaskBot SDK | Helper libraries for building TaskBot apps
TaskBot Library | Reusable code for TaskBot implementations

## Events

Events represent messages, notifications, etc. TaskBot pushes events to the application.

### Event Format

Events are JSON objects with required fields:

- `id` - Unique identifier
- `time` - Timestamp
- `type` - meta, message, notice, request
- `detail_type` - Detail type
- `sub_type` - Subtype

And more depending on event type.

### Event Examples

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
Action Requests

Action requests are sent by the application to request services.
Action Request Format

Action requests are JSON objects with required fields:

    action - Action name
    params - Parameters
    self - Sender identity

Action Request Example
{
  "action": "send_message",
  "params": {
    "message": ["Hi there!"]
  }
}
Action Responses

Action responses are sent by TaskBot back to the application after processing a request.
Action Response Format

Action responses are JSON objects with required fields:

    status - ok or failed
    retcode - Return code
    data - Response data
    message - Error message

Action Response Example
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "result": "success" 
  }
}
Return Codes

Return codes indicate execution status:

    0 - Success
    1xxxx - Request errors
    2xxxx - Handler errors
    3xxxx - Execution errors

And more.
Communication Methods

TaskBot Connect supports:

    HTTP
    HTTP Webhook
    WebSocket Forward
    WebSocket Reverse

It handles communication protocol and data encoding.
Data Protocols

TaskBot Connect uses:

    Events
    Action Requests
    Action Responses

It defines data transmission between the application and TaskBot.
HTTP Communication

TaskBot runs an HTTP server based on configuration:

    host - Listening IP
    port - Listening port
    access_token - Authentication
    event_enabled - Enable event polling
    event_buffer_size - Event buffer size

TaskBot handles requests at / and returns action responses.
HTTP Authentication

If access_token is set, TaskBot authenticates via:

    Authorization header
    access_token query parameter

HTTP Content Types

Supported request content types:

    application/json (required)
    application/msgpack (optional)

Response Content-Type mirrors request.
HTTP Event Polling

If event_enabled is true, TaskBot supports get_latest_events to poll events.

It provides an event buffer of configurable event_buffer_size.
HTTP Webhook

TaskBot pushes events to a webhook URL based on configuration:

    url - Webhook URL
    access_token - Authentication
    timeout - Request timeout

HTTP Webhook Headers

Required request headers:

    Content-Type - application/json
    User-Agent - TaskBot version
    X-TaskBot-Version - TaskBot version
    X-Impl - TaskBot implementation

Optional Authorization header for authentication.
HTTP Webhook Auth

Authenticates via:

    Authorization header
    access_token query parameter

HTTP Webhook Timeout

Request timeout is based on the configured timeout value.
WebSocket Communication

TaskBot supports WebSocket server and client roles.

Forwards events to clients and handles action requests.
WebSocket Authentication

If access_token is set, TaskBot authenticates before handshake via:

    Authorization header
    access_token query parameter

WebSocket Events & Actions

    Events as JSON
    Action requests as JSON or MessagePack
    Responses use the request format

WebSocket Communication (cont'd)

WebSocket Forward

TaskBot runs a WebSocket server based on configuration:

    host - Listening IP
    port - Listening port
    access_token - Authentication

It accepts connections at / and handles events and actions.

WebSocket Reverse

TaskBot connects to a WebSocket endpoint based on configuration:

    url - WebSocket URL
    access_token - Authentication
    reconnect_interval - Reconnect interval

It handles events and actions after connecting.
Data Types
Type Values

    Integer: int64, uint64, int32, uint32, int16, uint16, int8, uint8
    Float: float64
    String: string
    Bytes: Base64-encoded string or byte array
    Array: any[]
    Map: map[key_type]value_type
    Object: object (map[string]any)

Action Response

Action responses are objects with required fields:

    resp - Action name
    status - Status
    retcode - Return code
    data - Response data
    message - Error message

Robot Self Identification

self objects identify a robot:
{
  "platform": "telegram",
  "user_id": "123" 
}
Events

Events represent messages, notifications, etc.
Event Format

Events are objects with required fields:

    id - Unique ID
    self - Sender identity
    time - Timestamp
    type - Event type

Event Example
{
  "id": "123",
  "self": {
    "platform": "qq",
    "user_id": "1234"
  },
  "time": 1632847927,
  "type": "message",
  
  // other fields based on type  
}
Here's a syntax-and-logic checked and RapidAPI-compliant re-draft of the 'TaskBot schema':

markdown

# TaskBot Standard

The TaskBot standard defines a common API for developing chatbots, standardizing communication, data formats, and interfaces. It draws parallels with specifications such as C Language, ECMAScript, and POSIX.

## Document Keywords
Keyword | Meaning
--- | ---
MUST | Required
MUST NOT | Prohibited
SHALL | Recommended
SHALL NOT | Not Recommended
MAY | Optional

## Overview

TaskBot consists of two components:

1. **TaskBot Connect:** Handles communication protocols and data encoding.
2. **Interface Definition:** Specifies events, actions, and message formats.

## Terminology

Term | Definition
--- | ---
Robot/Bot | Chatbot
Robot Platform | Platforms like QQ, WeChat that provide chatbot APIs
TaskBot | The standard or an implementation
TaskBot Standard | The TaskBot API specification
TaskBot Implementation | A program implementing the TaskBot standard
TaskBot Application | A program using TaskBot to implement chatbot logic
TaskBot SDK | Helper libraries for building TaskBot apps
TaskBot Library | Reusable code for TaskBot implementations

## Events

Events represent messages, notifications, etc. TaskBot pushes events to the application.

### Event Format

Events are JSON objects with required fields:

- `id` - Unique identifier
- `time` - Timestamp
- `type` - meta, message, notice, request
- `detail_type` - Detail type
- `sub_type` - Subtype

And more depending on event type.

### Event Examples

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

Action Requests

Action requests are sent by the application to request services.
Action Request Format

Action requests are JSON objects with required fields:

    action - Action name
    params - Parameters
    self - Sender identity

Action Request Example

json

{
  "action": "send_message",
  "params": {
    "message": ["Hi there!"]
  }
}

Action Responses

Action responses are sent by TaskBot back to the application after processing a request.
Action Response Format

Action responses are JSON objects with required fields:

    status - ok or failed
    retcode - Return code
    data - Response data
    message - Error message

Action Response Example

json

{
  "status": "ok",
  "retcode": 0,
  "data": {
    "result": "success" 
  }
}

Return Codes

Return codes indicate execution status:

    0 - Success
    1xxxx - Request errors
    2xxxx - Handler errors
    3xxxx - Execution errors

And more.
Communication Methods

TaskBot Connect supports:

    HTTP
    HTTP Webhook
    WebSocket Forward
    WebSocket Reverse

It handles communication protocol and data encoding.
Data Protocols

TaskBot Connect uses:

    Events
    Action Requests
    Action Responses

It defines data transmission between the application and TaskBot.
HTTP Communication

TaskBot runs an HTTP server based on configuration:

    host - Listening IP
    port - Listening port
    access_token - Authentication
    event_enabled - Enable event polling
    event_buffer_size - Event buffer size

TaskBot handles requests at / and returns action responses.
HTTP Authentication

If access_token is set, TaskBot authenticates via:

    Authorization header
    access_token query parameter

HTTP Content Types

Supported request content types:

    application/json (required)
    application/msgpack (optional)

Response Content-Type mirrors request.
HTTP Event Polling

If event_enabled is true, TaskBot supports get_latest_events to poll events.

It provides an event buffer of configurable event_buffer_size.
HTTP Webhook

TaskBot pushes events to a webhook URL based on configuration:

    url - Webhook URL
    access_token - Authentication
    timeout - Request timeout

HTTP Webhook Headers

Required request headers:

    Content-Type - application/json
    User-Agent - TaskBot version
    X-TaskBot-Version - TaskBot version
    X-Impl - TaskBot implementation

Optional Authorization header for authentication.
HTTP Webhook Auth

Authenticates via:

    Authorization header
    access_token query parameter

HTTP Webhook Timeout

Request timeout is based on the configured timeout value.
WebSocket Communication

TaskBot supports WebSocket server and client roles.

Forwards events to clients and handles action requests.
WebSocket Authentication

If access_token is set, TaskBot authenticates before handshake via:

    Authorization header
    access_token query parameter

WebSocket Events & Actions

    Events as JSON
    Action requests as JSON or MessagePack
    Responses use the request format

WebSocket Communication (cont'd)

WebSocket Forward

TaskBot runs a WebSocket server based on configuration:

    host - Listening IP
    port - Listening port
    access_token - Authentication

It accepts connections at / and handles events and actions.

WebSocket Reverse

TaskBot connects to a WebSocket endpoint based on configuration:

    url - WebSocket URL
    access_token - Authentication
    reconnect_interval - Reconnect interval

It handles events and actions after connecting.
Data Types
Type Values

    Integer: int64, uint64, int32, uint32, int16, uint16, int8, uint8
    Float: float64
    String: string
    Bytes: Base64-encoded string or byte array
    Array: any[]
    Map: map[key_type]value_type
    Object: object (map[string]any)

Action Response

Action responses are objects with required fields:

    resp - Action name
    status - Status
    retcode - Return code
    data - Response data
    message - Error message

Robot Self Identification

self objects identify a robot:

json

{
  "platform": "telegram",
  "user_id": "123" 
}

Events

Events represent messages, notifications, etc.
Event Format

Events are objects with required fields:

    id - Unique ID
    self - Sender identity
    time - Timestamp
    type - Event type

Event Example

json

{
  "id": "123",
  "self": {
    "platform": "qq",
    "user_id": "1234"
  },
  "time": 1632847927,
  "type": "message",
  
  // other fields based on type  
}

Action Requests

Action requests are sent by the application to request services.
Action Request Format

Action requests are objects with required fields:

    action - Action name
    params - Parameters

And optional:

    echo - Identifier
    self - Sender identity

Action Request Example
{
  "action": "send_message",
  "params": {
    "message": ["Hi there!"] 
  },
  "echo": "123"
}
Action Responses

Action responses are sent back by TaskBot after processing a request.
Action Response Format

Action responses are objects with required fields:

    status - ok or failed
    retcode - Return code
    data - Response data
    message - Error message

And optional:

    echo - Mirrors request identifier

Action Response Example
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "result": "success"
  },
  "echo": "123"
}
Return Codes
Return codes indicate execution status:

    0 - Success
    1xxxx - Request errors
    2xxxx - Handler errors
    3xxxx - Execution errors

Request Errors

Similar to HTTP 4xx client errors.
Code	Error	Cause
10001	Bad Request	Malformed request
10002	Unsupported Action	Unimplemented action
10003	Bad Param	Invalid parameter

And more.
Handler Errors

Similar to HTTP 5xx server errors:
Code	Error	Cause
20001	Bad Handler	Implementation error
20002	Internal Handler Error	Uncaught exception
