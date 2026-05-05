import pytest

SAMPLE = """\
10.0.0.1 - - [15/Mar/2026:10:23:45 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.2 - - [15/Mar/2026:10:23:46 +0000] "POST /api/login HTTP/1.1" 401 128 "https://a.com" "curl/7.81"
10.0.0.1 - - [15/Mar/2026:10:24:00 +0000] "GET /favicon.ico HTTP/1.1" 404 - "-" "Mozilla/5.0"
10.0.0.3 - - [15/Mar/2026:14:05:00 +0000] "GET /health HTTP/1.1" 500 256 "-" "bot"
"""


@pytest.fixture
def sample_log(tmp_path):
    p = tmp_path / "access.log"
    p.write_text(SAMPLE, encoding="utf-8")
    return p


@pytest.fixture
def invalid_log(tmp_path):
    p = tmp_path / "bad.log"
    p.write_text("ligne totalement invalide\n" + SAMPLE, encoding="utf-8")
    return p
