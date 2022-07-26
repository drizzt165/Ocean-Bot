import math


def truncateEmbedValue(value):
    """Check that an embed string doesn't exceed discord embed character limit of 1024."""
    extension = '...\n\nMessage exceeds embed limits'
    maxLen = 1024
    if len(value) > maxLen:
        return value[:(maxLen-len(extension))] + extension
    else:
        return value


def format_YY_MM_DD(days):
    """
    Translate days amount into a string representing
    'X years, Y months, Z days ago'

    """
    dateString = ''
    if days > 365:
        years = math.floor(days/365)
        days -= (365*years)
        dateString += f"{years} years, "
        if days > 30:
            months = math.floor(days/30)
            days -= (30*months)
            dateString += f"{months} months"
    elif days > 30:
        months = math.floor(days/30)
        days -= (30*months)
        dateString += f"{months} months, {days} days"
    else:
        dateString += f"{days} days"
    dateString += " ago"
    return dateString
