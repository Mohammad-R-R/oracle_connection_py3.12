# My Library

A simple library for handling connections with customizable file readers and data parsers.

## Installation

You can install the library using pip:


## Usage

```python
from my_library import SimpleFileReader, SimpleConnectionDataParser, Connection

file_reader = SimpleFileReader('path/to/file.txt')
parser = SimpleConnectionDataParser()
connection = Connection(file_reader, parser)

username = connection.get_username()
password = connection.get_password()
dns = connection.get_dns()
