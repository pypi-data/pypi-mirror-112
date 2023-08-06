from typing import Any, Tuple
from collections import defaultdict
from datetime import datetime


# seasons=months mapping
seasons = [3, 3, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
DATE_FORMAT = '%Y-%m-%d'


def _prep_default(value: str) -> Tuple[bool, Any]:
    return True, value


def _prep_organic(value: str) -> Tuple[bool, str]:
    if not isinstance(value, bool):
        return False, value

    return True, 'organic' if value else 'conventional'


def _prep_date(value: str) -> Tuple[bool, int]:
    try:
        month = datetime.strptime(value, DATE_FORMAT).month
    except ValueError as e:
        return False, value

    return True, seasons[month - 1]


preprocess_function = defaultdict(lambda: _prep_default)
preprocess_function['organic'] = _prep_organic
preprocess_function['date'] = _prep_date
