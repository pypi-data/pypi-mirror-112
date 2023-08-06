from vakantie.calendar_info import *

holi = Holidays()
print(holi.get_holidays(years='2021, 2020', country='Bangladesh'))


# building wheel
# python setup.py sdist bdist_wheel

# checking
# tar tzf dist/vakantie-0.0.x.tar.gz
# twine check dist/*

# uploading
# twine upload --skip-existing dist/*