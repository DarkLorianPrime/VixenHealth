from sqlalchemy import TypeDecorator, String


class ByteString(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if not isinstance(value, bytes):
            raise TypeError("ByteString columns support only bytes values.")

        return value.decode()

    def process_result_value(self, value, dialect):
        return value.encode() if value else None
