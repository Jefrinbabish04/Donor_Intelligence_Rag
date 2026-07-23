class HistoryFormatter:

    def format(self, history):
        lines = []

        for message in history:
            lines.append(f"{message['role'].title()}: {message['content']}")

        return "\n".join(lines)
