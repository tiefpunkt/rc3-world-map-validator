import requests
import argparse

# Globals

map_failed = set()
map_ok = set()
map_to_parse = set()
map_parsed = set()

# Functions

def url_clean(url):
    #return url.replace("//","/").replace("https:/","https://").split("#")[0]
    return url.split("#")[0]

def check_url(url):
    if url in map_failed:
        return False
    if url in map_ok:
        return True

    try:
        r = requests.head(url)
    except requests.exceptions.ConnectionError:
        map_failed.add(url)
        return False

    if r.ok:
        map_ok.add(url)
        map_to_parse.add(url)
        return True
    else:
        map_failed.add(url)
        return False

def parse_map(url, print_success = False):
    if url in map_parsed:
        try:
            map_to_parse.remove(url)
        except KeyError:
            pass
        return

    if print_success:
        print(url)

    has_error = False

    r = requests.get(url)
    data = r.json()

    for layer in data["layers"]:
        if "properties" in layer:
            for prop in layer["properties"]:
                if prop["name"] == "exitSceneUrl" or prop["name"] == "exitUrl":
                    next = requests.compat.urljoin(url, prop["value"])
                    next = url_clean(next)
                    is_ok = check_url(next)

                    if is_ok:
                        if print_success:
                            print("  + %s" % next)
                    else:
                        if not print_success and not has_error:
                            print(url)
                        print("  - %s" % next)
                        has_error = True

    map_parsed.add(url)
    try:
        map_to_parse.remove(url)
    except KeyError:
        pass

parser = argparse.ArgumentParser(description='Validate rC3.world maps')
parser.add_argument("url", help="URL of the map to parser")
parser.add_argument('--recursive', "-r", action="store_true",
                    help='Recurse into other maps')
parser.add_argument("--verbose", "-v", action="store_true",
                    help='Print successes as well as failures')

args = parser.parse_args()

#start = "https://lobby.maps.at.rc3.world//maps/erfas-south.json"

url = url_clean(args.url)

parse_map(url, args.verbose)

if args.recursive:
    while len(map_to_parse) > 0:
        for url in list(map_to_parse):
            parse_map(url)
