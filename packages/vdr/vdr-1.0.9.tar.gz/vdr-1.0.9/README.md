
# VDR

VDR is a Python library to simulate a VDR (Voyage Data Recorder).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install vdr.

```bash
pip install vdr
```

## Usage
You first need to configure your VDR that will receive all the data.
```python
import vdr

VDR = vdr.Vdr('/home/USER')                         # Create the VDR with its storage path
VDR.add_connection("localhost", 12345, 'ECDIS')     # Create socket connection called 'ECDIS'
VDR.add_connection("localhost", 12346, 'nmea')      # Create socket connection called 'nmea'

# Initialize threads with each data type that connections will received
ecdis = vdr.ReceivingFrame(VDR, "ECDIS")
nmea = vdr.ReceivingNmea(VDR, "nmea")

# Start threads, ready to receive and store data
ecdis.start()
nmea.start()
```

Then, the library proposed different kind of agent to facilitate data emission.
### Frame Agent
```python
import screenagent

agent = screenagent.ScreenAgent("localhost", 12345)
agent.send_screenshot()


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)