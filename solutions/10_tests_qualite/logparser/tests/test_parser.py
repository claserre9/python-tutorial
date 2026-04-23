import pytest

from logparser.parser import parse_line, parse_file, ParseError


def test_parse_line_ok():
    line = (
        '10.0.0.1 - - [15/Mar/2026:10:23:45 +0000] '
        '"GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"'
    )
    entry = parse_line(line)
    assert entry.ip == "10.0.0.1"
    assert entry.method == "GET"
    assert entry.path == "/index.html"
    assert entry.status == 200
    assert entry.size == 1024


def test_parse_line_size_tiret():
    line = (
        '10.0.0.1 - - [15/Mar/2026:10:23:45 +0000] '
        '"GET /f HTTP/1.1" 404 - "-" "x"'
    )
    assert parse_line(line).size == 0


@pytest.mark.parametrize("bad", [
    "",
    "pas du tout un log",
    '10.0.0.1 - - [invalide] "GET /x HTTP/1.1" 200 1 "-" "x"',
])
def test_parse_line_invalid(bad):
    with pytest.raises(ParseError):
        parse_line(bad)


def test_parse_file_skip(sample_log):
    entries = list(parse_file(sample_log))
    assert len(entries) == 4


def test_parse_file_invalid_skip(invalid_log):
    entries = list(parse_file(invalid_log, skip_invalid=True))
    assert len(entries) == 4       # la ligne invalide est ignorée


def test_parse_file_invalid_raise(invalid_log):
    with pytest.raises(ParseError):
        list(parse_file(invalid_log, skip_invalid=False))
