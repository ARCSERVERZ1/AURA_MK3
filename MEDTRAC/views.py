from rest_framework.response import Response
from MEDTRAC.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
import pytz
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
import json

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


def food_tracker_home(requests):
    print("Medtrac requests")
    return render(requests, 'Medtrac_Logfood.html')


@api_view(['POST'])
def log_food_data(requests):
    data = json.loads(requests.data)
    # print(data , type(data))
    user = data["user_name"]

    for category in data:
        if category != 'user_name':
            if not data[category]['skipped'] :
                print(category)
                print(data[category]['qty'])
                print(data[category]['summary'])
                print(data[category]['datetime'])
                print(data[category]['category'])
                save_data = MealDataLog (
                    user = user ,
                    food_qty = data[category]['qty'] ,
                    food_description = data[category]['summary'] ,
                    food_type = data[category]['category'],
                    food_category =category ,
                    date = datetime.now() ,
                    time_stamp =  data[category]['datetime'] ,
                    updated_by = requests.user.username
                    )
                save_data.save()

    return JsonResponse({'Result': 'Data Updated'}, safe=False)
