from abc import ABC, abstractmethod

class ConnectionDataParser(ABC):
    @abstractmethod
    def parse(self, line):
        pass

class SimpleConnectionDataParser(ConnectionDataParser):
    def parse(self, line):
        try:
            username = line.split("/", 1)[0]
            password = line.split("/", 1)[1].split("@")[0]
            dns = line.split("/", 1)[1].split("@")[1]
            return {'username': username, 'password': password, 'dns': dns}
        except IndexError:
            raise ValueError("Line format is incorrect")
