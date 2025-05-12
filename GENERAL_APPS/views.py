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
    return JsonResponse({"status":"true"}, safe=False)

    # return JsonResponse({"Res": requests.POST.get('TempLocation')} , safe=False)


def test_run(requests):
    return render( requests ,'Gen_Test.html')

def rag_executor(query):
    counter = 0
    db.child('INS1').child('query').set(query)
    db.child('INS1').child('status').set('set')
    while True:
        counter = counter+1
        if counter > 10:
            return {'response': 'Time Out'}
        trig = db.child('INS1').child('status').get()
        if trig.val() == 'end':
            res = db.child('INS1').child('query_res').get()
            return { 'response': res.val()}
        time.sleep(1)



@api_view(['POST'])
def home_query(request):
    print(request.data)
    if request.data['model'] == 'Rag':
        res = rag_executor(request.data['query'])
        return JsonResponse( res, safe=False)


    return JsonResponse( request.data, safe=False)