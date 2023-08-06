# self_messages

libcmd is a Python library for creating and executing commands over a network socket connection.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libcmd.

```bash
pip install libcmd
```

## Usage

## Client code
```python

# CLIENT
from libcmd import libcmd
c = cmds()

output = c.send_socket(ip="localhost", port=8080, command="command", packet_size=1024, custom_arg="Bat")
print(output)
__________________
>>> True
```
## Server code
```python

# SERVER
from libcmd import libcmd
c = cmds()

def command(custom_arg: str):
    print(f"The command is {custom_arg}")
    return True

c.add("command", command)
c.start_socket()

```


## Contributing
Suck my cock and balls version 2

## License
[MIT](https://www.pornhub.com/)