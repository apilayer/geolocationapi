import io
import os
import shutil
import tarfile
import requests

GEOIP2_DB_URL = (
    "http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz"
)

r = requests.get(GEOIP2_DB_URL)
tar = tarfile.open(mode="r:gz", fileobj=io.BytesIO(r.content))
for member in tar.getmembers():
    if member.name.endswith("GeoLite2-Country.mmdb"):
        member.name = os.path.basename(member.name)
        tar.extract(member, path="data")
