from urllib import parse


def escape(raw):
    return parse.quote_plus(raw)
