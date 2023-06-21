import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
import calendar

class WeatherForecaster:

    API_DATE_FORMAT = '%Y-%m-%d'
    DEFAULT_LAT = 52.52
    DEFAULT_LNG = 13.41

    def __init__(self):
        self._monthly_rainfall_cache = {}

    def get_rainfall_for_next_n_months(self, n, lat=52.52, lng=13.41):
        today = datetime.date.today()
        current_month = datetime.date(today.year, today.month, 1)

        data = {}

        for i in range(n):
            current_month = datetime.datetime(current_month.year + int(current_month.month / 12), ((current_month.month % 12) + 1), 1)
            data[(current_month.year, current_month.month)] = self.get_rainfall_for_month(current_month.year, current_month.month, lat, lng)

        return data

    # # Get rainfall value for current month
    # def get_rainfall_for_current_month(self, lat=DEFAULT_LAT, lng=DEFAULT_LNG):
    #     today = datetime.date.today()
    #     return self.get_rainfall_for_month(today.year, today.month, lat, lng)

    def get_rainfall_for_month(self, year, month, lat=DEFAULT_LAT, lng=DEFAULT_LNG):
        _, end_day = calendar.monthrange(year, month)

        start_date = datetime.datetime(year, month, 1)
        end_date = datetime.datetime(year, month, end_day)

        return self.get_rainfall_for_dates(start_date, end_date, lat, lng)

    def get_rainfall_for_dates(self, start_date, end_date, lat=DEFAULT_LAT, lng=DEFAULT_LNG):

        # Get the start and end dates in the required format
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')

        # Get a string representation for weather data lat,lng,start_date,end_date in cache
        cache_str = f"{lat}-{lng}-{start_date}-{end_date}"

        # Return the previously cached forecast if present
        if cache_str in self._monthly_rainfall_cache:
            return self._monthly_rainfall_cache[cache_str]
        else:
            data_link = f"https://seasonal-api.open-meteo.com/v1/seasonal?latitude={lat}&longitude={lng}&daily=precipitation_sum&start_date={start_date}&end_date={end_date}"
            data = json.loads(requests.get(data_link).content)
            cleaned_data = [r for r in data["daily"]["precipitation_sum_member04"] if r != None]
            rainfall = sum(cleaned_data)            

            self._monthly_rainfall_cache[cache_str] = rainfall
            return rainfall

def main():
    wf = WeatherForecaster()
    print(wf.get_rainfall_for_next_n_months(8))
    print(wf.get_rainfall_for_next_n_months(8))

if __name__ == "__main__":
    main()