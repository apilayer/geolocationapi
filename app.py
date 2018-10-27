import ujson
import uvicorn

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import UJSONResponse

app = Starlette()
app.debug = False

# Middleware
app.add_middleware(CORSMiddleware, allow_origins=['*'])
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost:8000", "ipgeolocationapi.com"])


@app.on_event("startup")
async def startup():
    # Load countries into memory
    with open("countries.json") as f:
        app.countries = ujson.loads(f.read())


@app.route("/")
async def homepage(request):
    return UJSONResponse({"hello": "world"})


@app.route("/api/geocode")
async def homepage(request):
    country_code = request.headers.get("CF-IPCountry", "").upper()
    country = app.countries.get(country_code)
    if country:
        return UJSONResponse(country)
    else:
        return UJSONResponse({"message": "Could not geocode request."})


@app.route("/api/countries")
async def homepage(request):
    return UJSONResponse(app.countries)


@app.route("/api/countries/{country_code}")
async def homepage(request, country_code):
    country_code = country_code.upper()
    country = app.countries.get(country_code)
    if country:
        return UJSONResponse(country)
    else:
        return UJSONResponse({"message": "Country code not found."})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
