=====
csvmaker
=====

csvmaker is a Django app to generate csv from various types of file or structure

Quick start
-----------

use the function generate_csv_from_queryset

Given in input a QuerySet object, return the corresponding csv file

queryset:  QuerySet Object
csv_name: name for output csv (optional)

return response object

example:

from csvmaker.utils import generate_csv_from_queryset

queryset = PracticeDetails.objects.all()

csv_name = 'practice_details'

result = verify_cap(country, cap)


