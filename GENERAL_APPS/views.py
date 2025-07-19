from django.shortcuts import render
from django.http import JsonResponse
from requests import request
from .models import *
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
import json
from rest_framework.decorators import api_view, permission_classes
import pyrebase
import time
import re
from django.db.models import Count
import AURA_MK3.views as aura

# Create your views here.
firebaseConfig = {
    'apiKey': "AIzaSyAMoENs6AiTkSnAhuHuzwpGFkxeaAhGQB4",
    "authDomain": "aura-bifrost.firebaseapp.com",
    "databaseURL": "https://aura-bifrost-default-rtdb.firebaseio.com",
    "projectId": "aura-bifrost",
    "storageBucket": "aura-bifrost.appspot.com",
    "messagingSenderId": "774636407803",
    "appId": "1:774636407803:web:7710f0dec1c433a1b5d95e",
    "measurementId": "G-F8LXP6ZP1Q"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


def form_save_loc(requests):
    loc_data = locations_data.objects.all()

    context = {
        "locations": loc_data
    }

    return render(requests, 'Gen_LocHome.html', context)


def save_loc(requests):
    if requests.method == 'POST':

        print("{}{}{", requests.POST)

        if requests.POST['Transaction'] == 'New':
            new_loc_data = locations_data(
                location_name=requests.POST['locationName'],
                latitude=str(requests.POST['co_ordinates']).split('|')[0],
                longitude=str(requests.POST['co_ordinates']).split('|')[1],
                remarks=requests.POST['remarks'],
                group=requests.POST['group'],
                temp_location=requests.POST.get('tempLocation'),
                Active=requests.POST.get('active'),
                user_permission=requests.POST['userPermission'],
                time_stamp=datetime.now(),
                user=requests.user.username
            )
            new_loc_data.save()

        elif requests.POST['Transaction'] == 'Update':
            record_instance = locations_data.objects.filter(id=requests.POST['id'])
            record_instance.update(
                location_name=requests.POST['locationName'],
                remarks=requests.POST['remarks'],
                group=requests.POST['group'],
                temp_location=requests.POST.get('tempLocation'),
                Active=requests.POST.get('active'),
                user_permission=requests.POST['userPermission'],
                time_stamp=datetime.now(),
                user=requests.user.username
            )

        return redirect('location_home')


def get_data_by_id(requests):
    print(requests.body)
    request_data = json.loads(requests.body)
    data = locations_data.objects.filter(id=request_data['id'])
    print(list(data.values())[0])
    return JsonResponse(list(data.values())[0], safe=False)


def delete_by_id(requests):
    request_data = json.loads(requests.body)
    data = locations_data.objects.filter(id=request_data['id']).delete()
    return JsonResponse({"status": "true"}, safe=False)

    # return JsonResponse({"Res": requests.POST.get('TempLocation')} , safe=False)


def test_run(requests):
    return render(requests, 'Gen_Test.html')


def rag_executor(query):
    counter = 0
    db.child('INS1').child('query').set(query)
    db.child('INS1').child('status').set('set')
    while True:
        counter = counter + 1
        if counter > 10:
            return {'response': 'Time Out'}
        trig = db.child('INS1').child('status').get()
        if trig.val() == 'end':
            res = db.child('INS1').child('query_res').get()
            return {'response': res.val()}
        time.sleep(1)


@api_view(['POST'])
def home_query(request):
    print(request.data)
    if request.data['model'] == 'Rag':
        res = rag_executor(request.data['query'])
        return JsonResponse(res, safe=False)

    if request.data['model'] == 'Aura':  # Manage Checkist
        print(request.data)
        result = manage_checklist(request.data['query'], request.data['user'])
        return JsonResponse({"response": result['message']}, safe=False)


def save_check_list(result, user):
    try:
        for items in result['Items']:
            checklist(
                list_name=result['Name'],
                item=items,
                time_stamp=datetime.now(),
                user=user
            ).save()
        return {
            "status": True,
            "message": "CheckList Successfully Created !"
        }
    except Exception as e:
        return {
            "status": False,
            "message": f'{e}'
        }


def manage_checklist(text, user):
    res_message = {
        "status": False,
        "message": ""
    }

    text = text.strip()
    match = re.match(r'^\S+', text)
    template = {
        "Name": "",
        "Items": [],
        "message": '',
        "status": False
    }
    if match:
        if match.group().lower() == 'create':
            checklist_pattern = r'(?<=list)(.*?)(?=\n)'
            match = re.search(checklist_pattern, text)
            if match and len(match.group(1).strip()) > 1:
                template['Name'] = match.group(1).strip()
                checklist_item = r'(?<=\n)(.*?)(?=\n)'
                matches = re.findall(checklist_item, text)
                try:
                    for i, line in enumerate(matches, 1):
                        template['Items'].append(line.strip())
                    last_line_pattern = r'(?<=\n)[^\n]*$'
                    last_line_match = re.search(last_line_pattern, text)
                    if last_line_match:
                        template['Items'].append(last_line_match.group())
                    return save_check_list(template, user)

                except Exception as e:
                    res_message['status'] = True
                    res_message['message'] = f'Exception {e}'
            else:
                res_message['status'] = False
                res_message['message'] = "Opps template Name couldn't find in the prompt"
        elif match.group().lower() == 'delete':
            try:
                match = re.search(r'delete\s+(.+)', text, re.IGNORECASE)
                if match and len(match.group(1)) > 1:
                    print(match.group(1))
                    checklist.objects.filter(user=user, list_name=match.group(1)).delete()
                    res_message['status'] = True
                    res_message['message'] = f"deleted  {match.group(1)} successfully"
                else:
                    res_message['status'] = False
                    res_message['message'] = f"checklist name can read !"
            except Exception as e:
                res_message['status'] = False
                res_message['message'] = f"E- {e}"
        elif match.group().lower() == 'rename':
            try:
                match = re.search(r'rename\s+(.+)', text, re.IGNORECASE)
                if match and match.group(1).find("|") != -1:
                    list_names = match.group(1).split("|")
                    record = checklist.objects.filter(user=user, list_name=list_names[0])
                    record.update(
                        list_name =list_names[1]
                    )
                    res_message['status'] = True
                    res_message['message'] = f"{list_names[0]} renamed to {list_names[1]}"
                else:
                    res_message['status'] = False
                    res_message['message'] = f"checklist name can read !"
            except Exception as e:
                res_message['status'] = False
                res_message['message'] = f"E- {e}"
        else:
            res_message['status'] = False
            res_message['message'] = "Opps I am not sure about this prompt !"

        return res_message

    else:
        template['status'] = False
        template['message'] = "E-Opps I am not sure about this prompt !"


def checklist_dashboard(requests):
    context = {
        'user': requests.user.username,
        'users': aura.get_users(requests)

    }
    return render(requests, 'Gen_ChecklistDashBoard.html', context=context)


@api_view(['POST'])
def checklist_dashboard_data(requests):
    print(requests.data)
    data = list(checklist.objects.filter(user=requests.data['user']).values('list_name').annotate(count=Count('id')))
    print(data)
    return JsonResponse(data, safe=False)


@api_view(['POST'])
def checkpoint_data(requests):
    request_data = requests.data
    item_data = list(
        checklist.objects.filter(user=requests.data['user'], list_name=request_data['list_name']).values('item',
                                                                                                         'status',
                                                                                                         'id'))
    return JsonResponse({'item_data': item_data}, safe=False)


@api_view(['POST'])
def edited_check_point(requests):
    request_data = json.loads(requests.data)
    print(type(request_data))
    for item in request_data:
        print(item)
        record = checklist.objects.filter(id=item['id'])
        record.update(
            item=item['item'],
            status=item['status']
        )
    return JsonResponse({'item_data': 'True'}, safe=False)
