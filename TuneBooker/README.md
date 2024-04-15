# Dependencies

- python 3
- pip

On Ubuntu, run:

```
sudo apt install python3.8
sudo apt install python3-pip
```

You can change the python version above if 3.8 doesn't exists anymore.

## Python packages

All the dependencies will be listed on `setup.py`, to install them,
run at the TuneBooker directory:

```bash
python3 -m pip install -r requirements.txt
```

# Usage

The TuneBooker CLI is a simple interface to make requests and validate
responses to the DeeJay server. For detailed explanations on how to
use a certain command, use the `--help` flag.

To list the available operations, run:

```
python3 tune_booker.py --help
```

Each operation also has detailed explanations about it's arguments and
functionalities, e.g.:

```bash
python3 tune_booker.py create --help
```

will output:

```
usage: tune_booker.py create [-h] --host HOST --port PORT

Creates a new playlist and displays its returned ID.

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  Hostname or IP of the DeeJay server
  --port PORT  Port of the DeeJay server
```
