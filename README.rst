#To dump db
python manage.py dumpdata --indent=2 --output=mysite_data.json
#To load the dumped db
python manage.py loaddata mysite_data.json