import os
import unittest

from bamboo import (
    ASGIApp,
    ASGIHTTPEndpoint,
)
from bamboo.api import (
    BinaryApiData,
    FormApiData,
    JsonApiData,
)
from bamboo.request import http
from bamboo.sticky.http import data_format

from ..import get_log_name
from ..asgi_util import ASGIServerForm, ASGITestExecutor


app = ASGIApp()
PATH_SERVER_LOG = get_log_name(__file__)

HOST = "127.0.0.1"
PORT = 8000
URI_ROOT = f"http://{HOST}:{PORT}"
URI_BINARY = os.path.join(URI_ROOT, "binary")
URI_JSON = os.path.join(URI_ROOT, "json")
URI_FORM = os.path.join(URI_ROOT, "form")


class TestJsonApi(JsonApiData):

    username: str
    token: str


class TestFormApi(FormApiData):

    username: str
    token: str


IDEAL_DATA_BINARY = BinaryApiData(b"Hello, Client!")
IDEAL_DATA_JSON = TestJsonApi(username="hogehoge", token="token")
IDEAL_DATA_FORM = TestFormApi(username="hogehoge", token="token")


@app.route("binary")
class TestASGIBinaryApiEndpoint(ASGIHTTPEndpoint):

    @data_format(input=None, output=BinaryApiData)
    async def do_GET(self) -> None:
        self.send_api(IDEAL_DATA_BINARY)


@app.route("json")
class TestASGIJsonApiEndpoint(ASGIHTTPEndpoint):

    @data_format(input=None, output=TestJsonApi)
    async def do_GET(self) -> None:
        self.send_api(IDEAL_DATA_JSON)


@app.route("form")
class TestASGIFormApiEndpoint(ASGIHTTPEndpoint):

    @data_format(input=None, output=FormApiData)
    async def do_GET(self) -> None:
        self.send_api(IDEAL_DATA_FORM)


class TestASGISendApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        form = ASGIServerForm("", 8000, app, PATH_SERVER_LOG)
        cls.executor = ASGITestExecutor(form).start_serve()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.executor.close()

    def test_binary(self) -> None:
        with http.get(URI_BINARY) as res:
            self.assertTrue(res.ok)
            self.assertEqual(res.body, IDEAL_DATA_BINARY.__extract__())

    def test_json(self) -> None:
        with http.get(URI_JSON) as res:
            self.assertTrue(res.ok)
            self.assertEqual(res.body, IDEAL_DATA_JSON.__extract__())

    def test_form(self) -> None:
        with http.get(URI_FORM) as res:
            self.assertTrue(res.ok)
            self.assertEqual(res.body, IDEAL_DATA_FORM.__extract__())


if __name__ == "__main__":
    unittest.main()
