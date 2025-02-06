from abc import abstractmethod, ABC

class Extraction(ABC):
    @abstractmethod
    def extract(self) -> list:
        pass

