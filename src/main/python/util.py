import re


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = str(unicodedata.normalize('NFKD', value).encode('ascii', 'ignore'))
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    value = value[1:]  # Remove weird 'b' at the beginning

    return value
