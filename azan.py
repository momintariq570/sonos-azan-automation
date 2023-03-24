import requests
import time
from datetime import date
from datetime import datetime
import sonos

def get_azan_times(latitude, longitude, method=2):
    today = date.today()
    month = today.month
    day = today.day
    year = today.year
    url = "http://api.aladhan.com/v1/calendar?latitude={}&longitude={}&method={}&month={}&year={}".format(latitude, longitude, method, month, year)
    response = requests.get(url)
    data = response.json()
    # print(data["data"][day - 1]["date"]["readable"])
    print('---------------------------------------')
    return data["data"][day - 1]["timings"]

def run_azan_automation():
    while True:
        latitude = 39.3758027
        longitude = -77.3088401
        azan_times = get_azan_times(latitude, longitude)
        if is_azan_time(azan_times):
            print('IT IS AZAN TIME')
            sonos.run_sonos(volume=60)
            time.sleep(300)
        else:
            print('it is not azan time')
        time.sleep(30)

def is_azan_time(azan_times):
    dt = datetime.now()
    # dt = datetime(2023, 3, 4, 15, 34, 0, 0)
    time = dt.strftime('%H:%M')
    print('Time now: ' + time)
    fajr = str(azan_times["Fajr"]).rstrip(' (EDT)')
    dhuhr = str(azan_times["Dhuhr"]).rstrip(' (EDT)')
    asr = str(azan_times["Asr"]).rstrip(' (EDT)')
    maghrib = str(azan_times["Maghrib"]).rstrip(' (EDT)')
    isha = str(azan_times["Isha"]).rstrip(' (EDT)')

    print("Fajr:", fajr)
    print("Dhuhr:", dhuhr)
    print("Asr:", asr)
    print("Maghrib:", maghrib)
    print("Isha:", isha)

    if (time == fajr or time == dhuhr or time == asr or time == maghrib or time == isha):
        return True
    else:
        return False

if __name__ == '__main__':
    run_azan_automation()
    # Example usage
    # latitude = 39.3758027
    # longitude = -77.3088401
    # azan_times = get_azan_times(latitude, longitude)

    # print("Fajr:", azan_times["Fajr"])
    # print("Dhuhr:", azan_times["Dhuhr"])
    # print("Asr:", azan_times["Asr"])
    # print("Maghrib:", azan_times["Maghrib"])
    # print("Isha:", azan_times["Isha"])