from datetime import datetime, timedelta , timezone

rawdata = [
    {
        'id': 5,
        'user': 'Panisha',
        'food_qty': '5',
        'food_description': 'Pulao rice ',
        'food_type': 'Veg',
        'food_category': 'breakfast',
        'spare': '',
        'date': datetime.date(2025, 6, 22),
        'time_stamp': datetime.datetime(2025, 6, 22, 10, 0, tzinfo=datetime.timezone.utc),
        'updated_by': ''
    },
    {
        'id': 3,
        'user': 'Panisha',
        'food_qty': '8',
        'food_description': 'Mutton keema n rice',
        'food_type': 'Non-Veg',
        'food_category': 'lunch',
        'spare': '',
        'date': datetime.date(2025, 6, 22),
        'time_stamp': datetime.datetime(2025, 6, 22, 15, 0, tzinfo=datetime.timezone.utc),
        'updated_by': ''
    },
    {
        'id': 29,
        'user': 'Panisha',
        'food_qty': '8',
        'food_description': 'Kabab ,Lemon Chicken n rice ',
        'food_type': 'Non-Veg',
        'food_category': 'dinner',
        'spare': '',
        'date': datetime.date(2025, 6, 25),
        'time_stamp': datetime.datetime(2025, 6, 25, 20, 30, tzinfo=datetime.timezone.utc),
        'updated_by': ''
    },
    {
        'id': 30,
        'user': 'Panisha',
        'food_qty': '7',
        'food_description': 'Curd rice n prawns pickle ',
        'food_type': 'Non-Veg',
        'food_category': 'lunch',
        'spare': '',
        'date': datetime.date(2025, 6, 26),
        'time_stamp': datetime.datetime(2025, 6, 26, 13, 40, tzinfo=datetime.timezone.utc),
        'updated_by': ''
    },
    {
        'id': 31,
        'user': 'Panisha',
        'food_qty': '4',
        'food_description': 'Dosa',
        'food_type': 'Veg',
        'food_category': 'dinner',
        'spare': '',
        'date': datetime.date(2025, 6, 26),
        'time_stamp': datetime.datetime(2025, 6, 26, 21, 20, tzinfo=datetime.timezone.utc),
        'updated_by': ''
    },
    {
        'id': 35,
        'user': 'Panisha',
        'food_qty': '6',
        'food_description': 'Dosa',
        'food_type': 'Veg',
        'food_category': 'dinner',
        'spare': '',
        'date': datetime.date(2025, 6, 27),
        'time_stamp': datetime.datetime(2025, 6, 27, 21, 0, tzinfo=datetime.timezone.utc),
        'updated_by': ''
    },
    {
        'id': 36,
        'user': 'Panisha',
        'food_qty': '4',
        'food_description': 'testeer',
        'food_type': 'Veg',
        'food_category': 'breakfast',
        'spare': '',
        'date': datetime.date(2025, 6, 28),
        'time_stamp': datetime.datetime(2025, 6, 28, 11, 50, tzinfo=datetime.timezone.utc),
        'updated_by': ''
    }
]



start_date = '2025-06-21'
end_date = '2025-06-29'

template = {
    'breakfast': [],
    'lunch': [],
    'dinner': []
}

start = datetime.strptime(start_date, '%Y-%m-%d')
end = datetime.strptime(end_date, '%Y-%m-%d')
dates = []

for i in range((end - start).days + 1):
    dates.append((start + timedelta(days=i)).strftime('%Y-%m-%d'))

for i in dates:
    for meal in ['breakfast', 'lunch', 'dinner']:
        template[meal].append({'time': '00:00', 'category': 'skip', 'date': i})


print(template)

print("---------------------------------------------")
for entry in rawdata:
    print(entry)
