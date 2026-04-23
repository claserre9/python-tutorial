from logparser.analytics import top_ips, status_counts, erreurs_5xx, volume_par_heure
from logparser.parser import parse_file


def test_top_ips(sample_log):
    entries = list(parse_file(sample_log))
    top = top_ips(entries, 2)
    assert top[0] == ("10.0.0.1", 2)


def test_status_counts(sample_log):
    entries = list(parse_file(sample_log))
    counts = status_counts(entries)
    assert counts == {200: 1, 401: 1, 404: 1, 500: 1}


def test_erreurs_5xx(sample_log):
    entries = list(parse_file(sample_log))
    errs = list(erreurs_5xx(entries))
    assert len(errs) == 1
    assert errs[0].status == 500


def test_volume_par_heure(sample_log):
    entries = list(parse_file(sample_log))
    par_heure = volume_par_heure(entries)
    assert par_heure[10] == 3
    assert par_heure[14] == 1
