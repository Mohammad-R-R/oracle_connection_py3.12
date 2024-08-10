from abc import ABC, abstractmethod

class FileReader(ABC):
    @abstractmethod
    def read_line(self):
        pass

class SimpleFileReader(FileReader):
    def __init__(self, file_name):
        self.file_name = file_name

    def read_line(self):
        with open(self.file_name, 'r') as f:
            return f.readline().strip()
