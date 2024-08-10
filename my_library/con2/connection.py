from abc import ABC, abstractmethod

class FileReader(ABC):
    @abstractmethod
    def read_line(self):
        """Read a line from a file."""
        pass

class SimpleFileReader(FileReader):
    def __init__(self, file_name):
        self.file_name = file_name

    def read_line(self):
        with open(self.file_name, 'r') as f:
            return f.readline().strip()

class ConnectionDataParser(ABC):
    @abstractmethod
    def parse(self, line):
        """Parse a line of connection data."""
        pass

class SimpleConnectionDataParser(ConnectionDataParser):
    def parse(self, line):
        try:
            username, rest = line.split("/", 1)
            password, dns = rest.split("@", 1)
            return {'username': username, 'password': password, 'dns': dns}
        except ValueError:
            raise ValueError("Line format is incorrect")

class Connection:
    def __init__(self, file_reader: FileReader, parser: ConnectionDataParser):
        self.file_reader = file_reader
        self.parser = parser

    def get_username(self):
        return self._get_connection_data()['username']

    def get_password(self):
        return self._get_connection_data()['password']

    def get_dns(self):
        return self._get_connection_data()['dns']

    def _get_connection_data(self):
        line = self.file_reader.read_line()
        if not line:
            raise ValueError("File is empty")
        return self.parser.parse(line)
