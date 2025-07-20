from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from DEM import views as dem_views
from DOCMA import views as docma_views
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from DEM import models as dem_models
from DOCMA import models as docma_models
from GENERAL_APPS import models as gen_models
from MEDTRAC import models as medtrac_models


def diagnostics():
    print(os.getcwd())
    folder_path = os.path.dirname(os.getcwd())
    folder_name = os.path.basename(folder_path)
    folder_size = sum(os.path.getsize(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, file)))
    creation_time = os.path.getctime(folder_path)
    modification_time = os.path.getmtime(folder_path)

    # Print folder properties
    print("Folder Name:", folder_name)
    print("Folder Size (in bytes):", folder_size / (1024 ** 2))
    print("Creation Time:", creation_time)
    print("Modification Time:", modification_time)


def login(request):
    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        if user == 'Admin':
            pass
            # return redirect('/home')
        print(user.username)

    if request.method == 'POST':
        name = request.POST['UserName']
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password)

        if user is not None:
            auth.login(request, user)
            print("Logged in as ", user)
            # dem_views.speilspalz(request)
            # return render(request, 'dem_dashboard.html')
            return redirect('/home')
        else:

            print("login failed")
            messages.info(request, "Check User name or password")
            return render(request, "Login.html")
    else:
        pass

    return render(request, 'Login.html')


@login_required()
def home_page(request):
    # diagnostics()
    menu_bar = docma_views.home_menu_req()

    # Get the user's last name
    # print(request.user.last_name , "--------lst------------")
    # print(user.username , "--------use------------")
    # print(user.email , "--------em------------")

    context = {
        'menu_bar': menu_bar,
        'user': request.user.username

    }

    return render(request, "home.html", context)


def get_users(requests):
    lastname = requests.user.last_name
    users = User.objects.all()
    user_list = [str(requests.user.first_name)]
    for user in users:
        if str(user.last_name).strip().lower() == str(
                lastname).strip().lower() and requests.user.first_name != user.first_name:
            user_list.append(user.first_name)
    return user_list


@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def rag_data(requests):
    def validate_json_date_range(data):
        try:
            start = datetime.strptime(data['start_date'], '%Y-%m-%d')
            end = datetime.strptime(data['end_date'], '%Y-%m-%d')
            start_of_day = datetime.combine(start.date(), datetime.min.time())  # 00:00:00
            end_of_day = datetime.combine(end.date(), datetime.max.time())  # 23:59:59.999999

            dates = {
                "start_date": str(start),
                "end_date": str(end),
                "start_timestamp": str(start_of_day),
                "end_timestamp": str(end_of_day)
            }

            if end <= start:
                return [False, "Error: 'end_date' must be after 'start_date'."]
            delta_days = (end - start).days
            if delta_days > 50:
                return [False, f"Error: Date range is {delta_days} days, which exceeds the 50-day limit."]
            return [True, dates]
        except ValueError:
            return [False, "Error: Date format must be 'YYYY-MM-DD'."]

    res = validate_json_date_range(requests.data)

    rag_dict = {param: [] for param in requests.data['rag_parameters']}



    if res[0]:
        print(res)
        if "DEM" in requests.data["rag_parameters"]:
            in_json = list(dem_models.transactions_data.objects.filter(
                date__range=[requests.data['start_date'], requests.data['end_date']]).values())
            rag_dict['DEM'] = in_json
        if "FoodLog" in requests.data["rag_parameters"]:
            in_json = list(medtrac_models.MealDataLog.objects.filter(
                date__range=[requests.data['start_date'], requests.data['end_date']]).values())
            rag_dict['FoodLog'] = in_json
        if "MedicalIncidentRecord" in requests.data["rag_parameters"]:
            in_json = list(medtrac_models.HealthIncidentLogs.objects.filter(
                time_stamp__range=[res[1]['start_timestamp'], res[1]['end_timestamp']]).values())
            rag_dict['MedicalIncidentRecord'] = in_json
        if "Docma" in requests.data["rag_parameters"]:
            in_json = data = list(docma_models.docma_firebase.objects.values())
            rag_dict['Docma'] = in_json
        if "Checklist" in requests.data["rag_parameters"]:
            in_json = data = list(gen_models.checklist.objects.values())
            rag_dict['checklist'] = in_json
        if "Location" in requests.data["rag_parameters"]:
            in_json = data = list(gen_models.locations_data.objects.values())
            rag_dict['Location'] = in_json
    return JsonResponse({'Rag': rag_dict}, safe=False)
