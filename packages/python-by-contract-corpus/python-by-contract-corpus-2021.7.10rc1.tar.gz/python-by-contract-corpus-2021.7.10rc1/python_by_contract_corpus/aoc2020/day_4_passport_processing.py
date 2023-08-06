import sys
import re
from typing import List, Tuple

from icontract import require, ensure

_REQUIRED_KEYS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


@ensure(lambda text, result: len(result) == text.count("\n\n") + 1)
def blank_line_split(text: str) -> List[str]:
    """
    Split the text on a blank line.

    >>> blank_line_split('X\\nY\\n\\nZ')
    ['X\\nY', 'Z']
    """
    # NOTE: I tried to do a lookahead for the 2nd newline, but split doesn't take
    # a regex.
    return text.split("\n\n")


PASSPORT_RE = re.compile(r"\s*(\w+:(\S+))(\s+\w+:(\S+))*\s*")


@require(lambda text: PASSPORT_RE.fullmatch(text))
def parse_passport_entries(text: str) -> List[Tuple[str, str]]:
    """Parse the passport entries separated by a blank-line in ``text``."""
    result = []
    for tok in text.split():
        (k, v) = tok.split(":", 2)
        result.append((k, v))
    return result


@ensure(lambda entry, result: result == all(k in dict(entry) for k in _REQUIRED_KEYS))
def is_valid(entry: List[Tuple[str, str]]) -> bool:
    """Verify whether the passport entry is valid."""
    entry_keys = dict(entry).keys()
    return len(_REQUIRED_KEYS - entry_keys) == 0


@require(lambda batch: all(PASSPORT_RE.match(line) for line in blank_line_split(batch)))
@ensure(lambda result: result >= 0)
def count_valid(batch: str) -> int:
    """Count the number of valid passports in the ``batch``."""
    return sum(
        1
        for passport_text in blank_line_split(batch)
        if is_valid(parse_passport_entries(passport_text))
    )


if __name__ == "__main__":
    data = "".join(sys.stdin.readlines())
    print(count_valid(data))
