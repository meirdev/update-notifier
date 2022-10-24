from update_notifier.semver import parse_semver


def test_semver_lt_gt_1():
    a = parse_semver("1.0.0")
    b = parse_semver("2.0.0")
    c = parse_semver("2.1.1")

    assert a < b < c
    assert c > b > a


def test_semver_lt_gt_2():
    a = parse_semver("1.0.0-alpha")
    b = parse_semver("1.0.0")

    assert a < b
    assert b > a


def test_semver_lt_gt_3():
    a = parse_semver("1.0.0-alpha")
    b = parse_semver("1.0.0-alpha.1")
    c = parse_semver("1.0.0-alpha.beta")
    d = parse_semver("1.0.0-beta")
    e = parse_semver("1.0.0-beta.2")
    f = parse_semver("1.0.0-beta.11")
    g = parse_semver("1.0.0-rc.1")
    h = parse_semver("1.0.0")

    assert a < b < c < d < e < f < g < h
    assert h > g > f > e > d > c > b > a


def test_semver_eq():
    a = parse_semver("1.0.0-alpha")
    b = parse_semver("1.0.0-alpha")

    assert a == b


def test_semver_lte():
    a = parse_semver("1.0.0-alpha")
    b = parse_semver("1.0.0-alpha.1")
    c = parse_semver("1.0.0-alpha.1")

    assert a <= b <= c


def test_semver_gte():
    a = parse_semver("1.0.0-alpha")
    b = parse_semver("1.0.0-alpha.1")
    c = parse_semver("1.0.0-alpha.1")

    assert c >= b >= a
