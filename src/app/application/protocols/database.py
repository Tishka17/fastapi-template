from abc import ABC, abstractmethod


class DatabaseGateway(ABC):
    @abstractmethod
    def get_int(self) -> int:
        raise NotImplementedError
