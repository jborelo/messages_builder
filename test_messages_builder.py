import pytest
from MessagesBuilder import MessagesBuilder, Message, Role


class TestMessage:
    def test_to_dict(self):
        msg = Message(role=Role.USER, content="Hello")
        assert msg.to_dict() == {"role": "user", "content": "Hello"}

    def test_equality(self):
        msg1 = Message(role=Role.USER, content="Hello")
        msg2 = Message(role=Role.USER, content="Hello")
        msg2.id = 12
        assert MessagesBuilder.same_content_as(msg1, msg2)


class TestMessagesBuilder:
    def test_add_system(self):
        builder = MessagesBuilder()
        builder.add_system("You are helpful")
        assert len(builder._messages) == 1
        assert builder._messages[0].role == Role.SYSTEM
        assert builder._messages[0].content == "You are helpful"

    def test_add_user(self):
        builder = MessagesBuilder()
        builder.add_user("Hello")
        assert len(builder._messages) == 1
        assert builder._messages[0].role == Role.USER

    def test_add_assistant(self):
        builder = MessagesBuilder()
        builder.add_assistant("Hi there")
        assert len(builder._messages) == 1
        assert builder._messages[0].role == Role.ASSISTANT

    def test_add_message(self):
        builder = MessagesBuilder()
        builder.add_message(Role.FUNCTION, "some content")
        assert builder._messages[0].role == Role.FUNCTION

    def test_duplicate_consecutive_not_added(self):
        builder = MessagesBuilder()
        builder.add_user("Hello")
        builder.add_user("Hello")
        assert len(builder._messages) == 1

    def test_duplicate_non_consecutive_added(self):
        builder = MessagesBuilder()
        builder.add_user("Hello")
        builder.add_system("System")
        builder.add_user("Hello")
        assert len(builder._messages) == 3

    def test_reset(self):
        builder = MessagesBuilder()
        builder.add_system("System")
        builder.add_user("User")
        assert len(builder._messages) == 2
        builder.reset()
        assert len(builder._messages) == 0
        assert builder.generate_new_message_id() == 0

    def test_build(self):
        builder = MessagesBuilder()
        builder.add_system("System")
        builder.add_user("User")
        result = builder.build()
        assert result == [
            {"role": "system", "content": "System"},
            {"role": "user", "content": "User"},
        ]

    def test_build_returns_new_list(self):
        builder = MessagesBuilder()
        builder.add_user("Hello")
        result1 = builder.build()
        result2 = builder.build()
        assert result1 is not result2
