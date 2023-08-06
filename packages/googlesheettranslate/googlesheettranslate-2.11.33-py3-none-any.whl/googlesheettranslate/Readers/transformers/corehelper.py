import re


def RegexBoxNewLine(value: str) -> str:
    subst = ""
    normalizedValue = ""
    r1 = r"%newline%"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxDoubleQuote(value: str) -> str:
    subst = "\\\\\""
    normalizedValue = ""
    r1 = r"\""
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxSingleQuote(value: str) -> str:
    subst = "\\\\\""
    normalizedValue = ""
    r1 = r"\'"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxDoubleQuoteReverse(value: str) -> str:
    subst = '"'
    normalizedValue = ""
    r1 = r"\""
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxSingleQued(value: str) -> str:
    subst = "\\'"
    normalizedValue = ""
    r1 = r"'"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxAmp(value: str) -> str:
    subst = "&amp;"
    normalizedValue = ""
    r1 = r"&"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxSDF(value: str) -> str:
    subst = "%#$$$1"
    normalizedValue = ""
    r1 = r"%([sdf])"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxStrAt(value: str) -> str:
    normalizedValue = ""
    subst = "%@"
    r1 = r"%s"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxAt2String(value: str) -> str:
    normalizedValue = ""
    subst = "%s"
    r1 = r"%@"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxu0A00(value: str) -> str:
    normalizedValue = ""
    subst = "\\\u00A0"
    r1 = r"\u00A0"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE | re.MULTILINE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxCodeDot3(value: str) -> str:
    """
    do it a second time to fix values... ...like this (don't ask)
    @source: https://github.com/tntdigital/localize-with-spreadsheet/blob/master/core/Transformer.js
    @type {*}
    :param value:
    :return:
    """
    normalizedValue = ""
    subst = "$1&#8230;$3"
    r1 = r"([^\.]|^)(\.{3})([^\.]|$)"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxBR(value: str) -> str:
    normalizedValue = ""
    subst = "<br>"
    r1 = r"<BR>"
    result = re.sub(r1, subst, value, 0, re.MULTILINE | re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxDF(value: str) -> str:
    subst = "%$1"
    normalizedValue = ""
    r1 = r"%([@df])"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexLinkCase(value: str) -> str:
    regex = r"href=\"(.*?)\""
    matches = re.finditer(regex, value.lower(), re.MULTILINE)
    matched = False
    for matchNum, match in enumerate(matches):
        matched = True

    if matched:
        normalizedValue = "<![CDATA[{}]]>".format(value)
    else:
        normalizedValue = value

    return normalizedValue
