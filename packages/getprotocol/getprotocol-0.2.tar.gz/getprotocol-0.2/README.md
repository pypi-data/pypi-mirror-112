# GetProtocol

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=%40syed_umar)](https://twitter.com/syed__umar)

[contributors-shield]: https://img.shields.io/github/contributors/Anon-Exploiter/getprotocol.svg?style=flat-square
[contributors-url]: https://github.com/Anon-Exploiter/getprotocol/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/Anon-Exploiter/getprotocol.svg?style=flat-square
[issues-url]: https://github.com/Anon-Exploiter/getprotocol/issues

Simple script to get if a host is using http or https. Once the results come back, make sure to go through each and every line! Might contain bugs :cat:

### Tested On (OS & Python version)
- WSL2 - Ubuntu 20.04 LTS -- Python 3.8.5

### Downloading & Installation
```csharp
pip3 install getprotocol 
```

OR

```csharp
git clone https://github.com/Anon-Exploiter/getprotocol/
cd getprotocol/
python3 setup.py build 
python3 setup.py install --user
```

### Usage

Piping hosts `cat` from a file to the script:
```bash
cat hosts.txt | getprotocol
```

Get hosts from file and pass it to `getprotocol`:
```bash
getprotocol < hosts.txt
```

### Todos
- Add Colors
- Create a Docker image/Dockerfile
- Do more QA testing

### Filing Bugs/Contribution
Feel free to file a issue or create a PR for that issue if you come across any.
