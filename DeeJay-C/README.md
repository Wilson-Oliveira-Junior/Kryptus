# Dependencies

Install the following dependencies:

- libmicrohttpd
- libxml2
- lglib2.0

If you are on Ubuntu, you can install them with the following
commands:

## libmicrohttpd

```
# apt install libmicrohttpd12 libmicrohttpd-dev
```

## libxml2

```
# apt install libxml2 libxml2-dev
```

## lglib2.0

```
# apt install libglib2.0-0 libglib2.0-dev
```

# Usage

To build the server the makefile is already provided, so run at the
DeeJay-C directory:

```
make all
```

to build the project, or run:

```
make clean
```

to clean the project.

The generated program binary will be located at `bin/deejay`, to run,
execute:

```
./bin/deejay
```