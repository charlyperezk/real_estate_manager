from datetime import datetime
import calendar

# Hoy
now = datetime.now()

# Primer día del mes

start_date = datetime(now.year, now.month, 1)

# Último día del mes
last_day = calendar.monthrange(now.year, now.month)[1]
end_date = datetime(now.year, now.month, last_day, 23, 59, 59, 999999)

def current_period() -> str:
    return datetime.now().strftime("%Y-%m")