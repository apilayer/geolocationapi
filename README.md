# IP Geolocation API

IP Geolocation API is a free service for geocoding requests.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/madisvain/geolocationapi)

Request geocoding is done via [CloudFlare IP Geolocation](https://support.cloudflare.com/hc/en-us/articles/200168236-What-does-Cloudflare-IP-Geolocation-do-) to which additional information about the geolocated country is provided.


## Stack

IP Geolocation API is built upon Starlette to achieve high throughput. The current setup can asyncronously handle thousands of requests per second with very low system requirements.

#### Libraries used
* [Starlette](https://www.starlette.io/)
* [Uvicorn](https://www.uvicorn.org/)
* [uvloop](https://github.com/MagicStack/uvloop)
* [ultraJSON](https://github.com/esnme/ultrajson)


## Development
#### Install packages
```shell
pipenv install
```

#### Running the server
```shell
gunicorn app:app -k uvicorn.workers.UvicornWorker --reload
```

## Contributing
Thanks for your interest in the project! All pull requests are welcome from developers of all skill levels. To get started, simply fork the master branch on GitHub to your personal account and then clone the fork into your development environment.

Madis Väin (madisvain on Github, Twitter) is the original creator of the IP Geolocation API framework.

## License
MIT