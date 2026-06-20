from unittest.mock import MagicMock, patch

import requests

from src.tp3.utils.captcha import Captcha


def test_captcha_init():
    url = "http://example.com/captcha1/"
    captcha = Captcha(url)
    assert captcha.url == url
    assert captcha.image == b""
    assert captcha.value == ""


def test_capture_success():
    captcha = Captcha("http://example.com/captcha1/")
    mock_response = MagicMock()
    mock_response.content = b"fake_image"
    with patch.object(captcha._http_session, "get", return_value=mock_response):
        captcha.capture()
    assert captcha.image == b"fake_image"


def test_capture_failure():
    captcha = Captcha("http://example.com/captcha1/")
    with patch.object(captcha._http_session, "get", side_effect=requests.RequestException):
        captcha.capture()
    assert captcha.image == b""


def test_solve():
    captcha = Captcha("http://example.com/captcha1/")
    captcha.image = b"fake"
    with patch("src.tp3.utils.captcha.Image.open"), \
         patch("src.tp3.utils.captcha.pytesseract.image_to_string", return_value="123456\n"):
        captcha.solve()
    assert captcha.value == "123456"


def test_solve_empty_image():
    captcha = Captcha("http://example.com/captcha1/")
    captcha.solve()
    assert captcha.value == ""


def test_get_value():
    captcha = Captcha("http://example.com/captcha1/")
    captcha.value = "TEST123"
    assert captcha.get_value() == "TEST123"
