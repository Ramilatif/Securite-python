from unittest.mock import patch
from src.tp1.utils.lib import hello_world, choose_interface


def test_when_hello_world_then_return_hello_world():
    # Given
    string = "hello world"

    # When
    result = hello_world()

    # Then
    assert result == string


def test_when_choose_interface_then_return_selected_interface():
    # Given / When
    with patch("src.tp1.utils.lib.get_if_list", return_value=["eth0", "wlan0"]):
        with patch("builtins.input", return_value="0"):
            result = choose_interface()

    # Then
    assert result == "eth0"


def test_when_choose_interface_no_interfaces_then_return_empty_string():
    # Given / When
    with patch("src.tp1.utils.lib.get_if_list", return_value=[]):
        result = choose_interface()

    # Then
    assert result == ""


def test_when_choose_interface_eof_then_return_empty_string():
    # Given / When
    with patch("src.tp1.utils.lib.get_if_list", return_value=["eth0"]):
        with patch("builtins.input", side_effect=EOFError):
            result = choose_interface()

    # Then
    assert result == ""
