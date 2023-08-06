"""
"""
from typing import Tuple
import sys

import requests
import random
import webbrowser

from .constants import (
    NSFW_CATEGORIES,
    SFW_CATEGORIES,
    TYPES,
    CATEGORY,
    HELP_TEXT,
    API_BASE_URL,
    HELP_MSG,
)


def parse_args() -> Tuple[str, str]:
    type_ = 'sfw'
    category = random.sample(SFW_CATEGORIES, 1)[0]

    args = sys.argv
    if len(args) == 1:
        print(HELP_MSG)
    elif len(args) == 2:
        if args[1].lower() == 'help':
            print(HELP_TEXT)
            raise TypeError
        if args[1] in TYPES:
            type_ = args[1]
            category = random.sample(CATEGORY[type_], 1)[0]
        elif args[1] in SFW_CATEGORIES:
            type_ = 'sfw'
            category = args[1]
        elif args[1] in NSFW_CATEGORIES:
            type_ = 'nsfw'
            category = args[1]
        else:
            raise ValueError
    elif len(args) == 3:
        _, a, b = args
        if a in TYPES:
            type_ = a
            if b in CATEGORY[type_]:
                category = b
            else:
                raise ValueError
        elif b in TYPES:
            type_ = b
            if a in CATEGORY[type_]:
                category = a
            else:
                raise ValueError
        else:
            raise ValueError
    elif len(args) > 3:
        raise ValueError

    return type_.lower(), category.lower()


def show_waifu() -> None:
    try:
        type_, category = parse_args()
        url = f'{API_BASE_URL}/{type_}/{category}'
        res = requests.get(url).json()
        url = res['url']
        webbrowser.open(url)
    except ValueError:
        print(HELP_MSG)
    except TypeError:
        pass
    except Exception as err:
        print(f'Error {str(err)}')
