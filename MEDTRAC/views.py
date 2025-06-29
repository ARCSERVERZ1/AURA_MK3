from rest_framework.response import Response
from MEDTRAC.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
import pytz
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
import json
# import pandas as pd


def get_users(requests):
    lastname = requests.user.last_name
    users = User.objects.all()
    user_list = [str(requests.user.first_name)]
    for user in users:
        if str(user.last_name).strip().lower() == str(
                lastname).strip().lower() and requests.user.first_name != user.first_name:
            user_list.append(str(user.first_name).capitalize())
    return user_list


def medtrac_dashboard(requests):
    card_data = list(HealthIncidentLogs.objects.values())
    all_records = {}
    discomfort = list(config_discomfort.objects.values())
    for record in card_data:
        if record['user'] in all_records:
            all_records[record['user']].append(record)
        else:
            all_records[record['user']] = [record]

    res = {
        'users': get_users(requests),
        'discomforts': discomfort,
        'all_records': all_records
    }

    return render(requests, 'Medtrac_IT.html', context=res)


def add_health_incident(request):
    print(request.POST['Discomfort'])
    print(request.POST['Severity'])
    print(request.POST['Medication'])
    print(request.POST['Remarks'])
    print(request.POST['start_time'])
    print(request.POST['end_time'], "|")
    print(request.POST['After_Remarks'])

    HIL = HealthIncidentLogs(
        user=request.POST['Person'],
        discomfort=request.POST['Discomfort'],
        severity=request.POST['Severity'],
        apprx_start_time=request.POST['start_time'],
        apprx_end_time=request.POST['end_time'] if request.POST['end_time'] != "" else request.POST['start_time'],
        medication=request.POST['Medication'],
        while_remarks=request.POST['Remarks'],
        after_remarks=request.POST['After_Remarks'],
        time_stamp=datetime.now(pytz.timezone('Asia/Kolkata')),
        updated_by=request.user
    )
    HIL.save()

    return redirect('Medtrac_home')


@api_view(['POST'])
def delete_data_by_id(request):
    try:
        print(request.data)
        HealthIncidentLogs.objects.filter(id=request.data['id']).delete()
        return JsonResponse({'Result': 'Data Deleted'}, safe=False)
    except:
        return JsonResponse({'Result': 'Exception while Deleting data'}, safe=False)


@api_view(['POST'])
def get_data_by_id(requests):
    print(requests.data)
    data = list(HealthIncidentLogs.objects.filter(id=requests.data['id']).values())
    print(data[0]['apprx_start_time'])
    return JsonResponse({'Result': data}, safe=False)


@api_view(['POST'])
def update_data_by_id(request):
    try:
        print(request.data)

        record_data = HealthIncidentLogs.objects.filter(id=request.data['id'])

        record_data.update(
            user=request.data['Person'],
            discomfort=request.data['Discomfort'],
            severity=request.data['Severity'],
            apprx_start_time=request.data['start_time'],
            apprx_end_time=request.data['end_time'] if request.data['end_time'] != "" else request.data['start_time'],
            medication=request.data['Medication'],
            while_remarks=request.data['Remarks'],
            after_remarks=request.data['After_Remarks'],
            updated_by=request.user
        )

        return JsonResponse({'Result': 'Data Updated'}, safe=False)
    except Exception as e:
        return JsonResponse({'Result': f'Error {e}'}, safe=False)


def log_medtrac(requests):
    print(f"medtrac data save request")
    ist_time_stamp = datetime.now(pytz.timezone('Asia/Kolkata'))
    print(ist_time_stamp)

    if requests.method == 'POST':
        print(requests.POST['date'])

    log_data = medtrac_log(
        participant=requests.POST['Participant'],
        recorder=requests.POST['recorder'],
        test_parameter=requests.POST['Parameter'],
        v1=requests.POST['Value1'],
        v2=requests.POST['Value2'],
        v3=requests.POST['Value3'],
        date=requests.POST['date'],
        time_stamp=ist_time_stamp,
        remarks=requests.POST['remarks'],
        updated_by=requests.user.username
    )
    log_data.save()

    return render(requests, 'Medtrac_AddFoodLog.html')


@login_required()
def food_logger(request):
    if request.method == 'POST':
        food_qty = request.POST['food-qty']
        junk_rating = request.POST['junk-rating']
        satisfaction_level = request.POST['satisfaction-level']
        food_type = request.POST['food-type']
        time_stamp = request.POST['time']
        food_desc = ''
        user = request.user.username
        print(f'{food_qty}-{junk_rating}-{satisfaction_level}-{food_type}-{time_stamp}')

        if time_stamp == '':
            date = str(datetime.now().date())
            time_stamp = datetime.now()
        else:
            date = time_stamp.split('T')[0]

        def clean_data(data):
            return str(data).split(':')[1].strip()

        data = food_log(
            user=user,
            food_type=food_type,
            food_qty=clean_data(food_qty),
            junk_rating=clean_data(junk_rating),
            satisfaction_level=clean_data(satisfaction_level),
            food_description=food_desc,
            date=date,
            time_stamp=time_stamp,
            updated_by=''
        )

        data.save()
    return render(request, 'Medtrac_AddFoodLog.html')


def parse_date(date_str):
    try:
        # Try parsing as YYYY-MM-DD
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        # Fallback to full month name format
        return datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")


@api_view(['POST'])
def food_tracker_graph_data(requests):
    data = requests.data
    print(data)

    user = data['filter_user']
    start_date = parse_date(data['start_date'])
    end_date = parse_date(data['end_date'])
    print(user, start_date, end_date)
    grouped_data = {
        'breakfast': [],
        'lunch': [],
        'dinner': []
    }
    dates = []
    raw_data = MealDataLog.objects.filter(user=user, date__range=(start_date, end_date)).order_by('time_stamp')
    raw_data = list(raw_data.values())
    # grouped_data , dates = prepare_data(start_date, end_date, raw_data)
    for entry in raw_data:
        meal_type = entry['food_category']  # ensure key consistency
        try:
            if {'time': entry['time_stamp'].strftime('%H:%M'), 'category': entry['food_type'],
                'date': entry['date'].strftime('%Y-%m-%d')} in grouped_data[meal_type]:
                print('')
            else:
                # print("NEW" , entry['time_stamp'].strftime('%H:%M'), entry['food_type'],entry['date'].strftime('%Y-%m-%d'),)
                grouped_data[meal_type].append({
                    'time': entry['time_stamp'].strftime('%H:%M'),
                    'category': entry['food_type'],
                    'date': entry['date'].strftime('%Y-%m-%d'),
                })
                # print(grouped_data[meal_type])
                if entry['date'].strftime('%Y-%m-%d') not in dates:
                    dates.append(entry['date'].strftime('%Y-%m-%d'))
        except:
            pass

    # print(dates)

    response = {
        'meal_data': grouped_data,
        'labels': dates,
        'raw_data': raw_data,
        'user': user,
        'start_date': start_date,
        'end_date': end_date
    }
    # print({'meal_data': grouped_data, 'labels': list(dates)})
    return JsonResponse(response)


def food_tracker_home(requests):
    print("Medtrac requess")
    today = date.today()
    seven_days_ago = today - timedelta(days=10)
    # meal_data, dates = food_tracker_graph_data(requests ,requests.user.username, seven_days_ago, today)
    context = {
        'users': get_users(requests),
        'meal_list': ['breakfast', 'lunch', 'dinner'],
        'default_dates': [today, seven_days_ago]
    }

    return render(requests, 'Medtrac_Logfood.html', context)


@api_view(['POST'])
def log_food_data(requests):
    data = json.loads(requests.data)
    # print(data , type(data))
    user = data["user_name"]

    for category in data:
        if category != 'user_name':
            if not data[category]['skipped']:
                print(category)
                print(data[category]['qty'])
                print(data[category]['summary'])
                print(data[category]['datetime'])
                print(data[category]['category'])
                dt_str = data[category]['datetime']  # e.g., '2025-06-22T20:45'
                dt_obj = datetime.fromisoformat(dt_str)  # returns datetime.datetime(2025, 6, 22, 20, 45)

                save_data = MealDataLog(
                    user=user,
                    food_qty=data[category]['qty'],
                    food_description=data[category]['summary'],
                    food_type=data[category]['category'],
                    food_category=category,
                    date=dt_obj.date(),
                    time_stamp=data[category]['datetime'],
                    updated_by=requests.user.username
                )
                save_data.save()

    return JsonResponse({'Result': 'Data Updated'}, safe=False)


# def prepare_data(start_date, end_date, raw_data):
#     print("-----------------------------------DF-----------------------------------------------")
#     df = pd.DataFrame(raw_data)
#     print(df)
#     template = {
#         'breakfast': [],
#         'lunch': [],
#         'dinner': []
#     }
#
#     start = datetime.strptime(start_date, '%Y-%m-%d')
#     end = datetime.strptime(end_date, '%Y-%m-%d')
#     dates = []
#
#     for i in range((end - start).days + 1):
#         dates.append((start + timedelta(days=i)).strftime('%Y-%m-%d'))
#
#     for i in dates:
#         for meal in ['breakfast', 'lunch', 'dinner']:
#             p_date = datetime.strptime(i, '%Y-%m-%d').date()
#             food_types = df[(df['date'] == p_date) & (df['food_category'] == meal)]['food_type'].unique().tolist()
#             timestamp = df[(df['date'] == p_date) & (df['food_category'] == meal)]['time_stamp'].unique().tolist()
#             food_qty = df[(df['date'] == p_date) & (df['food_category'] == meal)]['food_qty'].unique().tolist()
#
#             if food_types:
#                 print(food_types[0], "|", p_date, meal)
#                 template[meal].append({'time': str(timestamp[0].strftime('%H:%M')), 'category': 'skip', 'date': i })
#             else:
#                 template[meal].append({'time': '00:00', 'category': 'skip', 'date': i})
#
#     return template , dates
