from .calendar_extractor import ExtractCalendar
import pandas as pd

class Holidays:
    def __init__(self,data_type="holiday_api"):
        self.data_type = data_type
        self.calender_extractor = ExtractCalendar() #years=self.years, country=self.country

    def get_holidays(self,  years="2021", country="bangladesh"):
        self.years = [int(year.strip()) for year in years.split(",")]
        holidays = None
        columns, holiday_data = self.calender_extractor.extract_calendar(self.years, country)
        # if self.data_type == "json":
        #     holidays = self._format_json(columns, holiday_data)
        if self.data_type == "holiday_api":
            holidays = self._format_holiday_api(holiday_data)
        elif self.data_type == "csv":
            holidays = self._format_dataframe(columns, holiday_data)
        return holidays

    def _format_json(self, columns, collection_of_holidays):
        holidays = {}
        transposed_data = []
        for data in collection_of_holidays:
            transposed_data += list(zip(*data))
        for i in range(len(columns)):
            holidays[columns[i]] = transposed_data[i]
        return holidays

    def _format_holiday_api(self, collection_of_holidays):
        holidays = {}
        # for country in self.countries:
        for year in self.years:
            data = collection_of_holidays[year]
            for holiday in data:
                holidays[holiday[1]] = holiday[2]

        return holidays

    def _format_dataframe(self, columns, data):
        # print(data)
        lis = []
        for key in data.keys():
            lis += data[key]

        return pd.DataFrame(data=lis, columns=columns)