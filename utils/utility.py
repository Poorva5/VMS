import uuid

class CoreUtil:
    def get_short_code():
        return str(uuid.uuid4()).replace("-", "")[:10].upper()