from app.application.protocols.database import DatabaseGateway


class StubDatabaseGateway(DatabaseGateway):
    def get_int(self) -> int:
        return 100
