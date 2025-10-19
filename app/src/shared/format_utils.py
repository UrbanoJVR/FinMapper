from flask import current_app
from flask_babel import format_currency


def format_currency_es(value, currency='€'):
    """
    Format currency value using Spanish locale formatting.
    
    Args:
        value: The numeric value to format (can be None, int, float, or Decimal)
        currency: The currency symbol (default: '€')
    
    Returns:
        Formatted currency string with Spanish locale (e.g., "1.234,56 €")
    """
    if value is None:
        return "0,00 €"
    
    try:
        # Try to use Flask-Babel's format_currency if we're in a Flask context
        if current_app:
            formatted = format_currency(value, currency)
            # Replace non-breaking space with regular space for consistency
            formatted = formatted.replace('\xa0', ' ')
            return formatted
    except (RuntimeError, AttributeError):
        # Fallback to manual formatting if not in Flask context or if Babel fails
        pass
    
    # Fallback: manual Spanish formatting
    # Convert to float to handle Decimal objects
    num = float(value)
    # Format with 2 decimal places
    formatted = f"{num:,.2f}"
    # Replace comma with temporary placeholder
    formatted = formatted.replace(",", "TEMP")
    # Replace period with comma (for decimals)
    formatted = formatted.replace(".", ",")
    # Replace temporary placeholder with period (for thousands)
    formatted = formatted.replace("TEMP", ".")
    
    # Add currency symbol
    return f"{formatted} €"
