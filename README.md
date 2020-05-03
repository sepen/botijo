# botijo

IRC bot written in Python with modules support

## Installation

Build and install
```
$ make
$ sudo make install
```

The command above will place the binary in _/usr/bin_. \
Alternatively you can also install it as a user in another path (i.e: _/opt/bin_)
```
$ sudo make install PREFIX=/opt
```

The example above will generate this tree:
```
  /opt/
   ├── bin
   │   └── botijo
   └── lib
       └── botijo
           ├── botijo.pyc
           ├── log.pyc
           ├── notes.pyc
           └── sysinfo.pyc
```

## Usage

```
  botijo <options>

  Where options are:
  -h, --help           Show this help information
  -V, --version        Show version information
  -v, --verbose        Print verbose messages
  --conf=CONFIG        Use alternate config file
  --host=SERVER        IRC server to connect
  --port=PORT          Port number of the server to connect
  --channels=CHANNELS  List of channels to join (separated by spaces)
  --mods=MODS          List of modules to enable (separated by commans)
  --nick=NICK          Nick name you want to use
```

## Examples

```
$ botijo --channels="#testchannel #mychannel" --nick=mybot
```