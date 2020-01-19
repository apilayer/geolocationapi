import io
import os
import shutil
import tarfile
import requests

GEOIP2_DB_URL = (
    "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&suffix=tar.gz&license_key=" + os.environ['LICENSE_KEY']
)

r = requests.get(GEOIP2_DB_URL)
tar = tarfile.open(mode="r:gz", fileobj=io.BytesIO(r.content))
for member in tar.getmembers():
    if member.name.endswith("GeoLite2-Country.mmdb"):
        member.name = os.path.basename(member.name)
        tar.extract(member, path="data")
