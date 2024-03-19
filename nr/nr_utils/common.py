from dateutil.parser import parse


def date_parse(string, agnostic=True, **kwargs):
    if agnostic or parse(string, **kwargs) == parse(
        string, yearfirst=True, **kwargs
    ) == parse(string, dayfirst=True, **kwargs):
        return parse(string, **kwargs)
    else:
        raise ValueError("The date was ambiguous: %s" % string)
