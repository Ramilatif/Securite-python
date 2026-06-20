from unittest.mock import MagicMock, patch

from src.tp3.utils.session import Session


def test_session_init():
    url = "http://example.com/captcha1/"
    session = Session(url)
    assert session.url == url
    assert session.captcha_value == ""
    assert session.flag_value == ""
    assert session.valid_flag == ""


def test_prepare_request():
    session = Session("http://example.com/captcha1/")
    with patch("src.tp3.utils.session.Captcha") as mock_captcha_class:
        mock_captcha = MagicMock()
        mock_captcha.get_value.return_value = "123456"
        mock_captcha_class.return_value = mock_captcha
        session.prepare_request()
    assert session.captcha_value == "123456"
    assert session.flag_value == "1000"


def test_submit_request():
    session = Session("http://example.com/captcha1/")
    session.captcha_value = "123456"
    session.flag_value = "1500"
    mock_response = MagicMock()
    with patch.object(session._http_session, "post", return_value=mock_response):
        session.submit_request()
    assert session._response == mock_response


def test_process_response_none():
    session = Session("http://example.com/captcha1/")
    assert session.process_response() is False


def test_process_response_invalid_captcha():
    session = Session("http://example.com/captcha1/")
    session._response = MagicMock()
    session._response.text = "<p>Invalid captcha</p>"
    assert session.process_response() is False


def test_process_response_incorrect_flag():
    session = Session("http://example.com/captcha1/")
    session._response = MagicMock()
    session._response.text = "<p>Incorrect flag.</p>"
    assert session.process_response() is False


def test_process_response_success():
    session = Session("http://example.com/captcha1/")
    session._response = MagicMock()
    session._response.text = "<p>Valid!</p>"
    session.flag_value = "1337"
    assert session.process_response() is True
    assert session.valid_flag == "1337"


def test_get_flag():
    session = Session("http://example.com/captcha1/")
    session.valid_flag = "FLAG123"
    assert session.get_flag() == "FLAG123"
