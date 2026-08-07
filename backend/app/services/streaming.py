import json


class StreamEvent:
    @staticmethod
    def status(message: str):
        return (
            json.dumps(
                {
                    "type": "status",
                    "message": message,
                }
            )
            + "\n"
        )

    @staticmethod
    def chunk(text: str):
        return (
            json.dumps(
                {
                    "type": "chunk",
                    "content": text,
                }
            )
            + "\n"
        )

    @staticmethod
    def done():
        return (
            json.dumps(
                {
                    "type": "done",
                }
            )
            + "\n"
        )

    @staticmethod
    def error(message: str):
        return (
            json.dumps(
                {
                    "type": "error",
                    "message": message,
                }
            )
            + "\n"
        )
