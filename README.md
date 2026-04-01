# MessagesBuilder

A lightweight Python library for building message lists for OpenAI API calls.

## Quick Start

Download `MessagesBuilder.py` and import directly:

```python
from MessagesBuilder import MessagesBuilder, Role

chat = MessagesBuilder()
```

## Usage

```python
from MessagesBuilder import MessagesBuilder, Role

chat = MessagesBuilder()

chat.add_system("You are a helpful SQL assistant.")
chat.add_user("Show me all users from table X")
chat.add_assistant("SELECT * FROM X;")

payload = chat.build()
```

## API

### Classes

**`Role`** - Enum for message roles:
- `Role.SYSTEM` - System message
- `Role.USER` - User message
- `Role.ASSISTANT` - Assistant message
- `Role.FUNCTION` - Function message
- `Role.TOOL` - Tool message

**`MessagesBuilder`** - Builder for constructing message lists

#### Methods

| Method | Description |
|--------|-------------|
| `add_message(role, content)` | Add a message with specified role |
| `add_system(content)` | Add a system message |
| `add_user(content)` | Add a user message |
| `add_assistant(content)` | Add an assistant message |
| `set_message_active(msgid, active)` | Enable/disable a message |
| `reset()` | Clear all messages |
| `build()` | Return messages as list of dicts |

### Output Format

`build()` returns a list of dictionaries suitable for OpenAI's chat completion API:

```python
[
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there!"}
]
```

## Features

- Prevents duplicate consecutive messages
- Messages can be activated/deactivated
- Auto-generated message IDs
- Clean dict output for API calls
