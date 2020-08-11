# ==============================================================================
# File: custom_functions.py
# Author: Francisco Cornejo-Garcia
# Description: Custom functions for data
# ==============================================================================

from datetime import datetime 
from dateutil.parser import parse

# Validate datetime format
def validate(datetime):
    try:
        return parse(datetime)
    except:
        return 'Error: Not a date'

# Find season
def findSeason(month, day):
    if month <= 3:
        season = 'winter'
    elif month >= 4 and month <= 6:
        season = 'spring'
    elif month >= 7 and month <= 9:
        season = 'summer'
    else:
        season = 'autumn'
        
    if month == 3 and day > 19:
        season = 'spring'
    elif month == 6 and day > 20:
        season = 'summer'
    elif month == 9 and day > 21:
        season = 'autumn'
    elif month == 12 and day > 20:
        season = 'winter'
    return season