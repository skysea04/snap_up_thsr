import re
from typing import Optional

import phonenumbers

local_map = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16,
             'H': 17, 'I': 34, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22,
             'O': 35, 'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28,
             'V': 29, 'W': 32, 'X': 30, 'Y': 31, 'Z': 33,
             }

PERSONAL_ID_PATTERN = r'^[A-Z][12]\d{8}$'
REGION_TW = 'TW'


def validate_personal_id(personal_id: str) -> bool:
    if not re.match(PERSONAL_ID_PATTERN, personal_id):
        return False

    digit_lst = list(map(int, str(local_map[personal_id[0]])))
    for i in range(1, 10):
        digit_lst.append(int(personal_id[i]))

    digit_sum = 0
    for i, d in enumerate(digit_lst):
        if i == 0:
            digit_sum += d

        digit_sum += d * (10 - i)

    if (digit_sum + int(personal_id[-1])) % 10 != 0:
        return False

    return True


def validate_n_format_phone(phone: str) -> Optional[str]:
    try:
        parsed_phone = phonenumbers.parse(phone, REGION_TW)
    except:
        return None

    if not phonenumbers.is_valid_number(parsed_phone):
        return None

    return f'0{parsed_phone.national_number}'
