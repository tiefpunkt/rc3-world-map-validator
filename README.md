# rc3.world map validator

Some maps in rc3.world don't exist so if you try to jump to them, you have to start all over again. This should check one or all maps against such issues.

## howto
```
git clone https://github.com/tiefpunkt/rc3-world-map-validator.git
cd rc3-world-map-validator
python3 -mvenv env
. env/bin/activate
pip install -r requirements.txt
python validate.py https://lobby.maps.at.rc3.world/main.json
```

You can also validate recursively, so validate all maps that are found within your given url, and keep on going like that:

```
python validate.py -r https://lobby.maps.at.rc3.world/main.json
```


Full options:

```
# python validate.py -h
usage: validate.py [-h] [--recursive] [--verbose] url

Validate rC3.world maps

positional arguments:
  url              URL of the map to parser

optional arguments:
  -h, --help        show this help message and exit
  --recursive, -r   Recurse into other maps
  --extract-urls -l Extract openWebsite URLs
  --verbose, -v     Print successes as well as failures
```
