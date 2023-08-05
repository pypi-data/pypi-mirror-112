import click
import os
import platform
import json

import requests

from .exceptions import (
    MdException, NotLoggedIn, ActionForbidden, RefreshTokenFailed
)
from .api import (
    AccountAPI, AuthAPI, AuthorAPI, ChapterAPI, GroupAPI, ListAPI, MangaAPI,
    MiscAPI, UserAPI, CoverAPI, UploadAPI
)
from .util import _is_token_expired, params_to_query, strip_nulls
from .endpoints import Endpoints


class APIHandler:
    UA = f"PyMyAPI on Python {platform.python_version()}"
    BASE = "https://api.mangadex.org"
    BASE = "https://api.mangadex.org.dev.mdcloud.moe"

    AUTH_FILE = ".mdauth"

    DEBUG = False

    def __init__(self, md):
        self.md = md
        self.user = None
        self._auth = None

        self.captcha = None

    def _save_auth(self):
        with open(self.AUTH_FILE, "w") as auth_file:
            json.dump({
                "user": self.user,
                "_auth": self._auth
            }, auth_file)

    def _load_auth(self):
        if not os.path.exists(self.AUTH_FILE):
            return

        with open(self.AUTH_FILE) as auth_file:
            try:
                auth = json.load(auth_file)
            except json.JSONDecodeError:
                return

        try:
            user = auth["user"]
            _auth = auth["_auth"]
        except KeyError:
            return

        self.user = user
        self._auth = _auth

        self._check_expired(silent_error=True)

    def _check_expired(self, silent_error=False):
        if self._auth is None:
            return

        if _is_token_expired(self._auth["session"]):
            try:
                self.md.auth.refresh()
            except MdException:
                if silent_error:
                    self.user = self._auth = None
                else:
                    raise RefreshTokenFailed()

    def _get_headers(self, auth: bool = True) -> dict:
        headers = {}
        if auth and self._auth is not None:
            headers["Authorization"] = "Bearer " + self._auth.get("session")
        if self.captcha is not None:
            headers["X-Captcha-Result"] = self.captcha
        headers["User-Agent"] = self.UA
        return headers

    def _make_request(
        self, action, body=None, params=None, urlparams=None, auth=True,
        files=None
    ):
        if params is not None:
            params = params_to_query(params)
        if action != Endpoints.Auth.REFRESH:
            self._check_expired()

        needs_base = not action[1].startswith(("http://", "https://"))
        url = (
            (self.BASE if needs_base else "")
            + action[1].format(**(urlparams or {}))
        )
        req = requests.request(
            action[0], url,
            json=None if action[0] == "GET" else strip_nulls(body),
            files=files,
            params=strip_nulls(params),
            headers=self._get_headers(auth)
        )
        if self.DEBUG:
            click.echo(click.style(f" -> {action[0]} {req.url}", fg="yellow"))
            from devtools import debug
            if action[0] != "GET":
                debug(strip_nulls(body))

            correlation = req.headers.get("X-Correlation-ID")
            if correlation:
                click.echo(click.style(
                    f" :: Correlation: {correlation}", fg="yellow"
                ))

        try:
            resp = {} if req.status_code == 204 else req.json()
        except json.decoder.JSONDecodeError:
            resp = None

        if req.status_code == 401:
            raise NotLoggedIn(resp)
        elif req.status_code == 403:
            raise ActionForbidden(resp)

        if req.status_code < 200 or req.status_code > 299:
            if resp is None:
                raise MdException(req.status_code)
            raise MdException(resp.get("errors", []))

        if not isinstance(resp, dict):
            return resp
        if "data" in resp:
            data = resp["data"]
            if "relationships" in resp:
                data["relationships"] = resp["relationships"]
            resp = data
        return resp

    def _authenticate(self, username, token):
        self._auth = token
        if token is None or username is not None:
            self.user = {"username": username}
        self._save_auth()

    def _get_refresh_token(self):
        if self._auth:
            return self._auth["refresh"]
        return None


class MdAPI:
    DEBUG = False

    def __init__(self):
        self.api = APIHandler(self)
        self.api.DEBUG = self.DEBUG

        self.account = AccountAPI(self, self.api)
        self.auth = AuthAPI(self, self.api)
        self.author = AuthorAPI(self, self.api)
        self.chapter = ChapterAPI(self, self.api)
        self.cover = CoverAPI(self, self.api)
        self.group = GroupAPI(self, self.api)
        self.list = ListAPI(self, self.api)
        self.manga = MangaAPI(self, self.api)
        self.misc = MiscAPI(self, self.api)
        self.user = UserAPI(self, self.api)
        self.upload = UploadAPI(self, self.api)

        self.api._load_auth()
