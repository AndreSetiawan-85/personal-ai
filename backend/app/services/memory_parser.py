import json
import re


class MemoryParser:
    def parse(self, text):
        if not text:
            return []

        text = text.strip()

        text = re.sub(
            r"```json",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = text.replace(
            "```",
            ""
        )

        start = text.find("[")
        end = text.rfind("]")

        if start == -1 or end == -1:
            return []

        json_text = text[start:end + 1]

        try:
            data = json.loads(json_text)

            if isinstance(data, list):
                return data

            return []

        except Exception:
            return []

memory_parser = MemoryParser()