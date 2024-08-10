class Connection:
    def __init__(self, file_reader, parser):
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
