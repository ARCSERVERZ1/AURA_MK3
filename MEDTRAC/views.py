from rest_framework.response import Response
from MEDTRAC.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
import pytz
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def get_users(requests):
    lastname = requests.user.last_name
    users = User.objects.all()
    user_list = [str(requests.user.first_name).capitalize()]
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
        'discomforts' :discomfort ,
        'all_records' : all_records
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
    res = {
        'users': get_users(request)
    }
    return render(request, 'Medtrac_IT.html', context=res)


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
