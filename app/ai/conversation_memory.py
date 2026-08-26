from collections import defaultdict


class ConversationMemory:

    _conversations = defaultdict(list)

    MAX_MESSAGES = 6

    @classmethod
    def add_message(
        cls,
        conversation_id: str,
        role: str,
        content: str
    ):

        cls._conversations[
            conversation_id
        ].append({
            "role": role,
            "content": content
        })

        # Keep only the most recent messages
        cls._conversations[
            conversation_id
        ] = cls._conversations[
            conversation_id
        ][-cls.MAX_MESSAGES:]


    @classmethod
    def get_history(
        cls,
        conversation_id: str
    ):

        return cls._conversations.get(
            conversation_id,
            []
        )


    @classmethod
    def clear(
        cls,
        conversation_id: str
    ):

        cls._conversations.pop(
            conversation_id,
            None
        )