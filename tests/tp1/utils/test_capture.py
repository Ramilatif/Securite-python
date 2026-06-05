from unittest.mock import patch, MagicMock
from src.tp1.utils.capture import Capture


@patch("src.tp1.utils.capture.choose_interface", return_value="eth0")
def test_capture_init(mock_choose):
    # When
    capture = Capture()

    # Then
    assert capture.interface == "eth0"
    assert capture.summary == ""
    assert capture.packets == []


@patch("src.tp1.utils.capture.choose_interface", return_value="eth0")
@patch("src.tp1.utils.capture.sniff", return_value=[MagicMock()])
def test_given_capture_when_capture_traffic_then_packets_stored(mock_sniff, mock_choose):
    # Given
    capture = Capture()

    # When
    capture.capture_traffic()

    # Then
    assert len(capture.packets) == 1
    mock_sniff.assert_called_once_with(iface="eth0", count=20)


@patch("src.tp1.utils.capture.choose_interface", return_value="")
def test_sort_network_protocols_empty_packets(mock_choose):
    # Given
    capture = Capture()

    # When
    result = capture.sort_network_protocols()

    # Then
    assert result == "{}"


@patch("src.tp1.utils.capture.choose_interface", return_value="")
def test_get_all_protocols_empty_packets(mock_choose):
    # Given
    capture = Capture()

    # When
    result = capture.get_all_protocols()

    # Then
    assert result == "{}"


@patch("src.tp1.utils.capture.choose_interface", return_value="")
def test_analyse(mock_choose):
    # Given
    capture = Capture()

    # When
    with (
        patch.object(capture, "get_all_protocols") as mock_get_protocols,
        patch.object(capture, "sort_network_protocols") as mock_sort,
        patch.object(capture, "_gen_summary") as mock_gen_summary,
    ):
        mock_gen_summary.return_value = "Test summary"
        capture.analyse("tcp")

    # Then
    mock_get_protocols.assert_called_once()
    mock_sort.assert_called_once()
    mock_gen_summary.assert_called_once()
    assert capture.summary == "Test summary"


@patch("src.tp1.utils.capture.choose_interface", return_value="")
def test_get_summary(mock_choose):
    # Given
    capture = Capture()
    capture.summary = "Test summary"

    # When
    result = capture.get_summary()

    # Then
    assert result == "Test summary"


@patch("src.tp1.utils.capture.choose_interface", return_value="")
def test_gen_summary_with_no_packets(mock_choose):
    # Given
    capture = Capture()

    # When
    result = capture._gen_summary()

    # Then
    assert "0" in result  # 0 paquets capturés
    assert "Résumé" in result
