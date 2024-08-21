from datetime import datetime, timedelta
time_now = datetime.now()

d = timedelta(days = 50)
a = time_now - d
print(a)