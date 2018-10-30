import os
import ujson
import uvicorn

from geoip2 import database
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import UJSONResponse

from middleware import WWWRedirectMiddleware

app = Starlette()
app.debug = False

# Middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost:8000",
        "ipgeolocationapi.com",
        "www.ipgeolocationapi.com",
    ],
)
app.add_middleware(WWWRedirectMiddleware)


@app.on_event("startup")
async def startup():
    # Open GeoIp2 database
    app.geoip2 = database.Reader(os.path.join("data", "GeoLite2-Country.mmdb"))
    # Load countries into memory
    with open(os.path.join("data", "countries.json")) as f:
        app.countries = ujson.loads(f.read())


@app.route("/")
async def homepage(request):
    return UJSONResponse({"hello": "world"})


@app.route("/api/geolocate")
async def geolocate(request):
    country_code = request.headers.get("CF-IPCountry", "").upper()
    country = app.countries.get(country_code)
    if country:
        return UJSONResponse(country)
    else:
        return UJSONResponse({"message": "Could not geocode request."})


@app.route("/api/geolocate/{ip}")
async def geolocate_ip(request):
    r = app.geoip2.country(request.path_params["ip"])
    country = app.countries.get(r.country.iso_code)
    if country:
        return UJSONResponse(country)
    else:
        return UJSONResponse({"message": "Could not geocode request."})


@app.route("/api/countries")
async def countries(request):
    return UJSONResponse(app.countries)


@app.route("/api/countries/{country_code}")
async def countries(request):
    country_code = request.path_params["country_code"].upper()
    country = app.countries.get(country_code)
    if country:
        return UJSONResponse(country)
    else:
        return UJSONResponse({"message": "Country code not found."})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
