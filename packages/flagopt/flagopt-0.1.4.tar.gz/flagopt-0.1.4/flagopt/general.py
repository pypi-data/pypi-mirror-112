
from . import abstract


__all__ = ('strip', 'clean', 'parse', 'group', 'split')


escape = '\\'


def strip(value, escape = escape, apply = str.strip, ghost = 1):

    value = apply(value)

    revert = len(escape)

    for index in range(ghost):
        if value.startswith(escape):
            value = value[revert:]
        if value.endswith(escape):
            value = value[:-revert]

    return value


def clean(values, strip = strip, empty = True):

    for value in values:

        value = strip(value)

        if not value and empty:

            continue

        yield value


def parse(values, *keys, escape = escape):

    kills = 0

    revert = len(escape)

    current = None

    for (valid, key, span) in abstract.parse(escape, values, keys):

        (start, stop) = (spot - kills for spot in span)

        if not valid:

            back = start - revert

            values = values[:back] + values[start:]

            kills += revert

            continue

        yield (current, values[:start])

        current = key

        values = values[stop:]

        kills += stop

    yield (current, values)


def group(values, *keys, parse = parse):

    (initial, *extras) = parse(values, *keys)

    (junk, initial) = initial

    store = {key: [] for key in keys}

    for (key, value) in extras:

        store[key].append(value)

    (keys, values) = zip(*store.items())

    return (initial, *values)


def split(values, key, group = group):

    (value, values) = group(values, key)

    values.insert(0, value)

    return values
