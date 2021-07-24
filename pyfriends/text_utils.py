import re


def strip_left_and_right_sides(value: str, rules: str = " \t\r\n") -> str:
    return value.strip(rules)


def newline_or_nbsp_to_space(value: str) -> str:
    return re.sub(r"(\r\n|\r|\n| )", " ", value)
