from datetime import date, datetime

from flask_babel import lazy_gettext, LazyString


def str_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%d/%m/%Y').date()


def get_translated_month_names() -> dict[int, LazyString]:
    """
    Returns a dictionary mapping month numbers (1-12) to their translated names.
    
    Returns:
        dict: {1: lazy_gettext('January'), 2: lazy_gettext('February'), ...}
    """
    return {
        1: lazy_gettext('January'), 2: lazy_gettext('February'), 3: lazy_gettext('March'),
        4: lazy_gettext('April'), 5: lazy_gettext('May'), 6: lazy_gettext('June'),
        7: lazy_gettext('July'), 8: lazy_gettext('August'), 9: lazy_gettext('September'),
        10: lazy_gettext('October'), 11: lazy_gettext('November'), 12: lazy_gettext('December')
    }
