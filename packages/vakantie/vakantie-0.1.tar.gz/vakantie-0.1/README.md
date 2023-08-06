This is a package for fetching holiday information of any country. This library can be used to get all the holidays of a
country. Even if a holiday is not pre-declared, one will still get the data for that holiday of any year.

### How to

```
import vakantie
holidays = vakantie.Holidays()
print(holidays.get_holidays(years=2021, country='Bangladesh'))
```

### Installation

```pip install vakantie```

### requirements

- lxml

### Available Years

Any year from 2015 upto now is available.

### Parameters of the class 'Holidays':
**output_type:** Currently, one can output the holidays in two ways - `csv` and `holiday_api`.

### Parameters of the 'get_holidays' method
**years:** This can take multiple years separated by comma(,).
**country:** Corrently it takes only a single year.

### Future plan
- Saving module
- Holidays for the states of the countries like the USA
- More output options

### Author
Labiba Kanij Rupty(labibakanij@gmail.com)
