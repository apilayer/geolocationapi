from starlette.datastructures import URL
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, ASGIInstance, Scope


class WWWRedirectMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    def __call__(self, scope: Scope) -> ASGIInstance:
        if scope["type"] in ("http"):

            host = None
            for key, value in scope["headers"]:
                if key == b"host":
                    host = value.decode("latin-1")
                    break
            print(host)
        
            """
            if host == "ipgeolocationapi.com":
                url = URL(scope=scope)
                url = url.replace(hostname="www.ipgeolocationapi.com")
                return RedirectResponse(url, status_code=301)
            """

        return self.app(scope)
