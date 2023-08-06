import multidict

from .general import *


__all__ = (*general.__all__, 'snip', 'draw', 'trace')


def snip(flags, value, apply = None):

    """
    Get recursive representation of arguments based on the flags.

    :param dict flags:
        Figure to use against value.
    :param str value:
        Content to derive results.
    :param func apply:
        Called on values, useful for sub-parsing.

    .. code-block:: py

        >>> flags = {'-s': 'size', '-t': {'-b': 'base', '-t': 'toppings'}}
        >>> value = 'big -t bbq \-t bacon -b tomato \-t mushroom'
        >>> args = snip(flags, value) # multidict
    """

    keys = flags.keys()

    store = multidict.MultiDict()

    for (key, value) in parse(value, *keys):
        value = strip(value)
        if key is None:
            if not value:
                continue
            key = next(iter(keys))
        item = flags[key]
        if isinstance(item, dict):
            value = snip(item, value, apply)
        elif apply:
            value = apply(item, value)
        store.add(key, value)

    return store


empty = ' '


clause = '()'


variable = '[]'


def draw(flags,
         empty = empty,
         clause = clause,
         variable = variable,
         apply = None):

    """
    Draw description on how these flags expect arguments.

    :param dict flags:
        Figure to derive result.
    :param str empty:
        Used to join chunks.
    :param str clause:
        Open and close of a sub-section.
    :param str variable:
        Open and close of variable names.
    :param func apply:
        Will be used on all variable names.

    .. code-block:: py

        >>> flags = {'-s': 'size', '-t': {'-b': 'base', '-t': 'toppings'}}
        >>> usage = draw(flags) # '-s [size] -t (-b [base] -t [toppings])'
    """

    glue = empty.join

    generate = abstract.draw(clause, variable, flags, glue, apply = apply)

    return glue(generate)


ignore = '{}|' + empty


def trace(value, ignore = ignore, clause = clause, variable = variable):

    """
    Get flags from the string; used for drawing and snipping.

    :param str value:
        The value to derive figure.
    :param str ignore:
        Skip any character found here.

    The rest are the same as in :func:`draw`.

    .. code-block:: py

        >>> usage = '-s [size] -t (-b {[base]} -t [toppings])'
        >>> args = trace(usage) # {'-s': 'size', '-t': {'-b': 'base', '-t': \
'toppings'}}
    """

    flags = {}

    buffer = ''

    level = 0

    upper = True

    for value in value:
        if upper:
            if value in ignore:
                continue
            if value == clause[0]:
                try:
                    if not level:
                        key = buffer
                        buffer = ''
                        continue
                finally:
                    level += 1
            if value == clause[1]:
                level -= 1
                if not level:
                    value = trace(buffer, ignore, clause, variable)
                    buffer = ''
                    flags[key] = value
                    continue
        if not level:
            if value == variable[0]:
                key = buffer
                buffer = ''
                upper = False
                continue
            if value == variable[1]:
                value = buffer
                buffer = ''
                flags[key] = value
                upper = True
                continue
        buffer += value

    return flags
