from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    async def get_connection(self):
        pass
