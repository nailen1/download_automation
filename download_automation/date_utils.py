from datetime import datetime, timedelta
from calendar import monthrange

def get_date_pairs_of_months(start_date, end_date):
    start_date = start_date.replace('-', '')
    end_date = end_date.replace('-', '')
    start_date = datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.strptime(end_date, '%Y%m%d')
    date_ranges = []

    current_date = start_date
    while current_date <= end_date:
        first_day = current_date.replace(day=1)
        last_day = current_date.replace(day=monthrange(current_date.year, current_date.month)[1])
        date_ranges.append((first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')))
        
        # Move to the next month
        next_month = current_date.month + 1 if current_date.month < 12 else 1
        next_year = current_date.year if next_month > 1 else current_date.year + 1
        current_date = current_date.replace(year=next_year, month=next_month)
    
    return date_ranges