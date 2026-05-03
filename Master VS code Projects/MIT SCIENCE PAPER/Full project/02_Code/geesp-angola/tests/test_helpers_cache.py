import time

from dashboard.utils.helpers import cache_decorator


def test_cache_decorator_caches():
    calls = {"count": 0}

    @cache_decorator(maxsize=8)
    def slow_inc(x):
        calls["count"] += 1
        return x + 1

    a = slow_inc(1)
    b = slow_inc(1)
    assert a == b == 2
    # second call should be cached so function only invoked once
    assert calls["count"] == 1
