import os
import jinja2
import ujson
import uvicorn

from geoip2 import database
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, UJSONResponse

from middleware import WWWRedirectMiddleware

app = Starlette()
app.debug = False

# Middleware
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "OPTIONS"]
)
app.add_middleware(WWWRedirectMiddleware)

# Static
app.mount("/static", StaticFiles(directory="static"))


@app.on_event("startup")
async def startup():
    # Open GeoIp2 database
    app.geoip2 = database.Reader(os.path.join("data", "GeoLite2-Country.mmdb"))
    # Load countries into memory
    with open(os.path.join("data", "countries.json")) as f:
        app.countries = ujson.loads(f.read())


@app.route("/", methods=["GET", "HEAD"])
async def homepage(request):
    path = os.path.join("templates", "index.html")
    with open(path, "r") as f:
        template = jinja2.Template(f.read())
        return HTMLResponse(template.render())


@app.route("/api/geolocate", methods=["GET", "HEAD"])
async def geolocate(request):
    country_code = request.headers.get("CF-IPCountry", "").upper()
    country = app.countries.get(country_code)
    if country:
        return UJSONResponse(country)
    else:
        return UJSONResponse({"message": "Could not geocode request."})


@app.route("/api/geolocate/{ip}", methods=["GET", "HEAD"])
async def geolocate_ip(request):
    r = app.geoip2.country(request.path_params["ip"])
    country = app.countries.get(r.country.iso_code)
    if country:
        return UJSONResponse(country)
    else:
        return UJSONResponse({"message": "Could not geocode request."})


@app.route("/api/countries", methods=["GET", "HEAD"])
async def countries_list(request):
    return UJSONResponse(app.countries)


@app.route("/api/countries/{country_code}", methods=["GET", "HEAD"])
async def countries_detail(request):
    country_code = request.path_params["country_code"].upper()
    country = app.countries.get(country_code)
    if country:
        return UJSONResponse(country)
    else:
        return UJSONResponse({"message": "Country code not found."})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
