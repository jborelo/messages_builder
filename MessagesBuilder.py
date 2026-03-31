from dataclasses import dataclass, field
from enum import Enum


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"


type Content = str
type MessageID = int


@dataclass
class Message:
    """
    Represents a single message in a conversation.
    """
    role: Role
    content: Content

    #
    id: MessageID = None
    active: bool = True

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role.value, "content": self.content}

    # def same_content_as(self, other: "Message") -> bool:
    #     if not isinstance(other, Message):
    #         return False
    #     return self.to_dict() == other.to_dict()
    #



@dataclass
class MessagesBuilder:
    """A builder class for constructing message lists for OpenAI API calls."""

    # default_factory to ensure each instance has its own list
    _messages: list[Message] = field(default_factory=list)
    _last_message_id: MessageID = -1

    @staticmethod
    def same_content_as(m1: Message, m2: Message) -> bool:
        return m1.role == m2.role and m1.content == m2.content

    def change_message_state(self, msgid: MessageID, active: bool) -> None:
        for msg in self._messages:
            if msg.id == msgid:
                msg.active = active
                break

    def generate_new_message_id(self) -> MessageID:
        return self._last_message_id + 1


    def get_last_active_message(self) -> Message | None:
        for msg in reversed(self._messages):
            if msg.active:
                return msg
        return None


    def _add_message(self, msg: Message) -> int | None:
        # add if empty ot not same as last
        if self._messages and  self.same_content_as(msg, self.get_last_active_message()):
            return None

        msg.id = self.generate_new_message_id()
        self._last_message_id = msg.id

        self._messages.append(msg)
        return msg.id



    def add_message(self, role: Role, content: str) -> MessageID:
        return self._add_message(Message(role=role, content=content))

    def add_system(self, content: str) -> MessageID:
        return self.add_message(Role.SYSTEM, content)

    def add_user(self, content: str) -> MessageID:
        return self.add_message(Role.USER, content)

    def add_assistant(self, content: str) -> MessageID:
        return self.add_message(Role.ASSISTANT, content)

    def reset(self) -> None:
        """Resets the message history by clearing all messages."""
        self._messages.clear()
        self._last_message_id = -1

    def build(self) -> list[dict[str, str]]:
        return [msg.to_dict() for msg in self._messages if msg.active]


# if __name__ == "__main__":
#     # --- PRZYKŁAD UŻYCIA ---
#
#     # Tworzenie historii rozmowy
#     chat = MessagesBuilder()
#
#     chat.add_system("Jesteś pomocnym asystentem SQL.")
#     chat.add_user("Jak wybrać wszystkich userów z tabeli X?")
#     chat.add_assistant("Użyj: SELECT * FROM X;")
#     chat.add_user("A jak ich posortować?")
#
#     # Gotowa lista do wysłania do client.chat.completions.create(...)
#     payload = chat.build()
#
#     print(payload)
