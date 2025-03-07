from datetime import datetime, timedelta
import json
import calendar

def load_holidays():
    with open('holidays.json', 'r') as f:
        return json.load(f)

def get_countries():
    holidays = load_holidays()
    return list(holidays.keys())

def get_years():
    return list(range(2024, 2026))

def is_weekend(date):
    return date.weekday() >= 5

def get_long_weekend_potentials(country, year):
    holidays = load_holidays()
    country_holidays = holidays[country][str(year)]
    
    potentials = []
    
    for holiday in country_holidays:
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
