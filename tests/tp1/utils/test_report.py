from unittest.mock import patch, MagicMock
from src.tp1.utils.report import Report


def test_report_init():
    # Given
    capture = MagicMock()
    filename = "test.pdf"
    summary = "Test summary"

    # When
    report = Report(capture, filename, summary)

    # Then
    assert report.capture == capture
    assert report.filename == filename
    assert report.title == "TITRE DU RAPPORT"
    assert report.summary == summary
    assert report.array == ""
    assert report.graph == ""


def test_concat_report():
    # Given
    report = Report(MagicMock(), "test.pdf", "Test summary")
    report.title = "Test Title"
    report.array = "Test Array"
    report.graph = "Test Graph"

    # When
    result = report.concat_report()

    # Then
    assert result == "Test TitleTest summaryTest ArrayTest Graph"


def test_save():
    # Given
    capture = MagicMock()
    report = Report(capture, "test.pdf", "Test summary")
    report.title = "Test Title"

    # When
    with patch("src.tp1.utils.report.FPDF") as mock_pdf_class:
        mock_pdf = MagicMock()
        mock_pdf_class.return_value = mock_pdf
        report.save("test.pdf")

    # Then
    mock_pdf.output.assert_called_once_with("test.pdf")


def test_generate_graph():
    # Given
    capture = MagicMock()
    capture.packets = []
    report = Report(capture, "test.pdf", "Test summary")

    # When
    with patch("src.tp1.utils.report.pygal.Bar") as mock_bar_class:
        mock_bar = MagicMock()
        mock_bar_class.return_value = mock_bar
        report.generate("graph")

    # Then
    assert report.graph.endswith("protocols_chart.svg")
    mock_bar.render_to_file.assert_called_once_with(report.graph)


def test_generate_array():
    # Given
    capture = MagicMock()
    capture.packets = []
    report = Report(capture, "test.pdf", "Test summary")

    # When
    report.generate("array")

    # Then
    assert "Protocole" in report.array
    assert "Source IP" in report.array


def test_generate_invalid_param():
    # Given
    report = Report(MagicMock(), "test.pdf", "Test summary")

    # When
    report.generate("invalid")

    # Then
    assert report.graph == ""
    assert report.array == ""
