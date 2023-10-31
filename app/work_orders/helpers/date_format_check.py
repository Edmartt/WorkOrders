import logging
import traceback
from datetime import date

def check_date_format(sent_date: str) -> None | Exception:

    try:
        date.fromisoformat(sent_date)
    except ValueError as ex:
        return ex
