from collections import deque


class ConversationMemory:

    def __init__(self, maxlen=10):
        self.history = deque(maxlen=maxlen)

    def add(self, role, content):
        self.history.append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_history(self):
        return list(self.history)

    def clear(self):
        self.history.clear()
