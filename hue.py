from config import Config
import flask
import json
import os
from ssdp import SSDP
from threading import Thread
import urllib3

config = None

config_file_paths = [
    os.path.dirname(os.path.realpath(__file__)) + "/config/default.cfg.local",
    "/etc/hue-adapter/default.cfg.local",
]

for config_file_path in config_file_paths:
    if os.path.isfile(config_file_path):
        config = Config(file(config_file_path))

if not config:
    print "Cannot find configuration file"
    exit(1)

app = flask.Flask(__name__)

@app.route("/setup.xml")
def get_setup_file():
    """Serve the SSDP setup file."""

    out = "<?xml version=\"1.0\"?>\n" + \
          "<root xmlns=\"urn:schemas-upnp-org:device-1-0\">\n" + \
          "<specVersion>\n" + \
          "<major>1</major>\n" + \
          "<minor>0</minor>\n" + \
          "</specVersion>\n" + \
          "<URLBase>http://%s:%d/</URLBase>\n" % (config.web.addr, config.web.port) + \
          "<device>\n" + \
          "<deviceType>urn:schemas-upnp-org:device:Basic:1</deviceType>\n" + \
          "<friendlyName>Philips Hue Emulator</friendlyName>\n" + \
          "<manufacturer>Royal Philips Electronics</manufacturer>\n" + \
          "<manufacturerURL></manufacturerURL>\n" + \
          "<modelDescription>Philips Hue Emulator</modelDescription>\n" + \
          "<modelName>Philips hue bridge 2012</modelName>\n" + \
          "<modelNumber>929000226503</modelNumber>\n" + \
          "<modelURL></modelURL>\n" + \
          "<serialNumber>00000000000000000001</serialNumber>\n" + \
          "<UDN>uuid:776c1cbc-790a-425f-a890-a761ec57513c</UDN>\n" + \
          "</device>\n" + \
          "</root>\n"

    return flask.Response(out, mimetype="text/xml")

@app.route("/api/<username>/lights", methods=["GET"])
def get_all_lights(username):
    """Get all lights"""

    out = {}

    for id, light in config.lights.iteritems():
        out[id] = {
            "state": {
                "on": False,
                "bri": 0,
                "hue": 0,
                "sat": 0,
                "xy": [0, 0],
                "ct": 0,
                "alert": "none",
                "effect": "none",
                "colormode": "hs",
                "reachable": True,
            },
            "type": "Extended color light",
            "name": light["name"],
            "modelid": "LCT001",
            "swversion": "6609461",
            "pointsymbol": {},
        }

    return flask.jsonify(out)

@app.route("/api/<username>/lights/<id>", methods=["GET"])
def get_light(username, id):
    """Get light attributes and state"""

    if id in config.lights:
        light = config.lights[id]
    else:
        return "", 3

    out = {
        "state": {
            "on": False,
            "bri": 0,
            "hue": 0,
            "sat": 0,
            "xy": [0, 0],
            "ct": 0,
            "alert": "none",
            "effect": "none",
            "colormode": "hs",
            "reachable": True,
        },
        "type": "Extended color light",
        "name": light["name"],
        "modelid": "LCT001",
        "swversion": "6609461",
        "pointsymbol": {},
    }

    return flask.jsonify(out)

@app.route("/api/<username>/lights/<id>/state", methods=["PUT"])
def set_lights_state(username, id):
    """Set light state"""

    if id in config.lights:
        light = config.lights[id]
    else:
        return "", 3

    data = flask.request.get_json(force=True)

    if not data or "on" not in data:
        return "", 6

    if data["on"]:
        url = light["on_url"]
    else:
        url = light["off_url"]

    try:
        http = urllib3.PoolManager()
        r = http.request("GET", url)
    except:
        return "", 901

    out = [
        {
            "success": {
                "/lights/" + id + "/state/on": data["on"]
            }
        }
    ]

    return flask.Response(json.dumps(out), mimetype="text/json")

if __name__ == "__main__":
    ssdp = SSDP(config.web.addr, config.web.port)
    ssdp_thread = Thread(target=ssdp.run)
    ssdp_thread.setDaemon(True)
    ssdp_thread.start()

    app.run(host=config.web.addr, port=config.web.port)
