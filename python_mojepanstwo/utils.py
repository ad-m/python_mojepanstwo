try:  # Python 2.x
    from urllib import quote
except ImportError:
    from urllib.parse import quote


def urlencode_php(data):
    """
    Convert a dict to a percent-encoded ASCII text string in PHP-like way.
    """
    output = []
    for key, value in data.items():
        if isinstance(value, dict):
            for key2, value2 in value.items():
                output.append("%s[%s]=%s" % (quote(str(key)),
                                             quote(str(key2)),
                                             quote(str(value2))))
        elif isinstance(value, list):
            for value in value:
                output.append("%s[]=%s" % (quote(str(key)),
                                           quote(str(value2))))
        else:
            output.append("%s=%s" % (quote(str(key)),
                                     quote(str(value))))

    return "&".join(output)
