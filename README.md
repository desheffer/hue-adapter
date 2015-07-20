# Hue adapter
Philips Hue API adapter for controlling non-Hue devices

The Amazon Echo now supports "Connected Home" devices, but its support is
quite limited.  This application serves as an adapter to any unsupported home
automation systems (e.g. openHAB), as long as they provide their own web API.

## Installation

You will need to copy `config/default.cfg` to `config/default.cfg.local`.
Then, adjust the list of `lights` and the `on_url` and `off_url` values needed
to control them.  You should generate a new UUID for each light that you add.

Once the application is set up and running, log into your Amazon Echo
(echo.amazon.com) and click "Discover devices".  The Echo should automatically
discover the adapter and add the devices from your configuration.
