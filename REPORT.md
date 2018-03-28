# Installation
1. clone this repo

2. migrate
```
python manage.py migrate
```
3. import csv
```
python manage.py import
```
4. runserver

# Issues
### CSV Import function
- no validation

For Example,
Confirm existence of user when importing consumption data.

- Data addition and update are not considered.

### Model
- no area & tariff master table.

- no Aggregate Tables

### View
- not responsible design

### Test

- no test about chart

- no test about models.Round

# technical decisions

### CSV import function
- Do not use arguments

I thought that the location of CSV should be fixed.

### added libraries
- django-graphos

A simple graph representation was enough, so I used this.

- django-pandas & pandas

Since the aggregated Queryset could not be handled by the graphos, it was used to convert from Queryset to Python list.

