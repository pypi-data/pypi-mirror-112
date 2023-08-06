# SCA11H
Simple wrapper over the [Muarata's Bed Sensor](https://www.murata.com/en-us/products/sensor/accel/overview/lineup/sca10h_11h/sca11h).
It's based on the [Hostless WLAN HTTP API specification](https://www.murata.com/en-us/products/sensor/accel/overview/lineup/sca10h_11h/sca11h).

## Usage

It can be used from a command line:
```shell
bcg-hostless-api --node=192.168.0.XXX get-bcg-pars
```

Or inside an application:
```python
from SCA11H.commands.bcg.GetParams import GetParams
parameters = GetParams(host='192.168.0.XXX').run()
print(parameters)
```