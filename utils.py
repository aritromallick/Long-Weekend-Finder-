from datetime import datetime, timedelta
import json
import calendar
from holiday_api import holiday_api

COUNTRY_CODE_MAP = {
    'India': 'IN',
    # Add more country mappings as needed
}

def get_countries():
    return list(COUNTRY_CODE_MAP.keys())

def get_years():
    return list(range(2024, 2031))  # Extended to 2030

def is_weekend(date):
    return date.weekday() >= 5

def get_holidays_for_month(country, year, month):
    country_code = COUNTRY_CODE_MAP[country]
    holidays = holiday_api.get_holidays(country_code, year)

    holiday_dates = set()
    for holiday in holidays:
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')
        if holiday_date.month == month:
            holiday_dates.add(holiday['date'])

    return holiday_dates

def get_long_weekend_potentials(country, year):
    country_code = COUNTRY_CODE_MAP[country]
    holidays = holiday_api.get_holidays(country_code, year)

    potentials = []

    for holiday in holidays:
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')

        # Check surrounding dates
        dates_to_check = [
            (holiday_date - timedelta(days=1)),
            (holiday_date + timedelta(days=1)),
            (holiday_date - timedelta(days=2)),
            (holiday_date + timedelta(days=2))
        ]

        for check_date in dates_to_check:
            if is_weekend(check_date):
                # Found a potential long weekend
                leaves_needed = []
                total_days = 1  # Count the holiday

                # Check if we need to take leaves between weekend and holiday
                start_date = min(holiday_date, check_date)
                end_date = max(holiday_date, check_date)

                current_date = start_date
                while current_date <= end_date:
                    if not is_weekend(current_date) and current_date != holiday_date:
                        leaves_needed.append(current_date.strftime('%Y-%m-%d'))
                    total_days += 1
                    current_date += timedelta(days=1)

                if len(leaves_needed) <= 2:  # Only consider if leaves needed are 2 or less
                    potentials.append({
                        'holiday': holiday['name'],
                        'holiday_date': holiday['date'],
                        'leaves_needed': leaves_needed,
                        'total_days': total_days,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': end_date.strftime('%Y-%m-%d')
                    })
                break  # Move to next holiday after finding first potential

    return potentials

def create_whatsapp_share_text(potential):
    text = f"🏖️ Long Weekend Plan!\n"
    text += f"Holiday: {potential['holiday']} ({potential['holiday_date']})\n"
    text += f"Duration: {potential['total_days']} days\n"
    text += f"From: {potential['start_date']} To: {potential['end_date']}\n"
    if potential['leaves_needed']:
        text += f"Leaves needed: {', '.join(potential['leaves_needed'])}"
    else:
        text += "No leaves needed! 🎉"
    return text