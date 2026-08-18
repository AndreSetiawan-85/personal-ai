import json
import re


class MemoryParser:
    def _clean(self, text):
        text = text.strip()
        text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
        text = text.replace("```", "")
        return text.strip()

    def parse_array(self, text):
        if not text:
            return []

        text = self._clean(text)
        start = text.find("[")
        end = text.rfind("]")

        if start == -1 or end == -1:
            return []

        try:
            data = json.loads(text[start:end + 1])
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def parse_object(self, text):
        if not text:
            return {}

        text = self._clean(text)
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            return {}

        try:
            data = json.loads(text[start:end + 1])
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    # alias biar kompatibel kalau ada kode lama yang manggil .parse()
    def parse(self, text):
        return self.parse_array(text)


memory_parser = MemoryParser()
