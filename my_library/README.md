# My Library

A simple library for handling connections with customizable file readers and data parsers.

## Installation

You can install the library using pip:


## Usage

```python
from my_library import Connection,SimpleFileReader,SimpleConnectionDataParser

file_reader = SimpleFileReader('connection.txt')
parser = SimpleConnectionDataParser()
connection = Connection(file_reader, parser)

username = connection.get_username()
password = connection.get_password()
dns = connection.get_dns()
```

and you should creat the connection.txt at 
my_project
	|---my_project
	|---my_app
	manage.py
	connection.
	
	and your connection should be like 
	name/password@ip:port:dns