# Hue adapter
Philips Hue API adapter for controlling non-Hue devices

The Amazon Echo now supports "Connected Home" devices, but its support is
quite limited.  This application serves as an adapter to any unsupported home
automation systems (e.g. openHAB).  It will wrap the target system--as long as
it provides its own web API--and expose it as if it were a Hue bridge.

## Installation

Run `pip -r requirements.txt` to install dependencies.

You will need to copy `config/default.cfg` to `config/default.cfg.local`.
Then, adjust the list of `lights` and the `on_url` and `off_url` values needed
to control them.  You should generate a new UUID for each light that you add.

Once the application is set up and running, log into the Amazon Echo dashboard
(http://echo.amazon.com), go to "Settings", "Connected Home", then click
"Discover devices".  The Echo should automatically discover the adapter and add
the devices from your configuration.

To make the application start at boot time, add the following to your crontab
(adjust paths accordingly):

    @reboot /usr/bin/python /usr/share/hue-adapter/hue.py > /var/log/hue-adapter.log 2>&1
