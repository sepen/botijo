# Botijo

IRC bot written in Python with modules support

## Installation

Botijo uses `Poetry` for Python dependency management (https://python-poetry.org/) so first of all you will need to run the install command from the `src` dir like this:
```
$ cd src
$ poetry install
```

Then you can build and install it by calling the Makefile from the top dir.
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

To configure your bot, you should edit the config file `botijo.conf` which contains default values.
This can be override with command line options.

Command line options and usage:
```
Usage: botijo <options>
Where options are:
 -h, --help           Show this help information
 -V, --version        Show version information
 -v, --verbose        Print verbose messages
 --conf=CONFIG        Use alternate config file (default: ~/.botijo.conf)
 --host=SERVER        IRC server to connect
 --port=PORT          Port number of the server to connect
 --channels=CHANNELS  List of channels to join (separated by spaces)
 --nick=NICK          Nick name you want to use
Example:
  botijo --host=localhost --channels='#test1 #test2' --nick=foo
```

Additionally you can run botijo like a system daemon, for this purpose `botijo.rc` is provided as an
example start script (use it at your own risk).