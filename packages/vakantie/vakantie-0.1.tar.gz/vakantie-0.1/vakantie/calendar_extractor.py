from bs4 import BeautifulSoup
import requests
import json
import re
import calendar
from datetime import date

class ExtractCalendar:
    def __init__(self):

        self.months = {month: index for index, month in enumerate(calendar.month_abbr) if month}

    def extract_calendar(self, years, country):
        holiday_information = {}
        self.years = years
        columns = None
        for year in self.years:
            columns, holiday_information[year] = self.extract_single_calendar(year, country)

        return columns, holiday_information
    def extract_single_calendar(self, year, country):
        url = f"https://www.officeholidays.com/countries/{country}/{year}"
        html_content = requests.get(url).text

        # Parse HTML code for the entire site
        soup = BeautifulSoup(html_content, "lxml")
        gdp = soup.find_all("table", attrs={"class": "country-table"})
        holiday_info = None
        columns = None

        for table in gdp:
            body = table.find_all("tr")
            head = body[0]
            web_data = body[1:]
            columns = []
            for item in head.find_all("th"):  # loop through all th elements
                # convert the th elements to text and strip "\n"
                item = (item.text).rstrip("\n")
                # append the clean column name to headings
                columns.append(item)

            holiday_info = []
            for row_num in range(len(web_data)):  # A row at a time
                row = []  # this will old entries for one row
                i = 0
                for row_item in web_data[row_num].find_all("td"):  # loop through all row entries

                    aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)

                    # print(row)
                    # print(aa)
                    if i == 1:
                        date_info = aa.split(" ")
                        aa = date(year=year, month=self.months[date_info[0]], day=int(date_info[1]))

                    row.append(aa)
                    i += 1
                # append one row to all_rows
                holiday_info.append(row)
                # holiday_info[holidate.isoformat()] = row
        return columns, holiday_info
