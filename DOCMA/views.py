from django.shortcuts import render
import os , time
from datetime import datetime
from .models import *
from django.http import JsonResponse
import json, os
from django.contrib.auth.models import User, auth
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
import string, random
import pyrebase
import shutil

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
bucket = firebase.storage()



def encrypt_value(value):
    x = 0
    rand = str(random.randint(1000000, 9999999))
    rand = [i for i in rand]
    for index, digit in enumerate(rand):
        if index in [2, 5, 8]:
            rand.insert(index, str(value)[x])
            x = x + 1
    return ''.join([i for i in rand])



@login_required()
def doc_manger_home(request):
    # document_type = doc_type.objects.values_list('type', flat=True)

    if str(request.user.last_name).lower() == 'baswa':
        document_type = docma_firebase.objects.values_list('type', flat=True).distinct()
        context = {
            'doc_type': document_type
        }
    else:
        # document_type = docma_firebase.objects.values_list('type', flat=True).distinct()
        document_type = docma_firebase.objects.filter(updated_by= str(request.user)).values_list('type', flat=True).distinct()
        context = {
            'doc_type': document_type
        }
    print(context)
    return render(request, "Docma_Category.html", context)


def add_document(request):
    document_holders = doc_holder.objects.values_list('Holder', flat=True)
    document_type = doc_type.objects.values_list('type', flat=True)
    print(document_holders, "-----------------------------------------")
    context = {
        'document_holders': document_holders,
        'document_type': document_type
    }

    return render(request, "Docma_AddDocument.html", context)


# @login_required()
# def doc_manager(request):
#     document_holders = doc_holder.objects.values_list('Holder', flat=True)
#     document_type = doc_type.objects.values_list('type', flat=True)
#     print(document_holders, "-----------------------------------------")
#     context = {
#         'document_holders': document_holders,
#         'document_type': document_type
#     }
#
#     return render(request, "docma_home.html", context)
#     # return render(request, "doc_manager.html" , context)



def save_uploaded_file(file):
    # Define the directory where you want to save the uploaded files
    upload_dir = 'path/to/save/files/'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    with open(os.path.join(upload_dir, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def add_doc_type(request, new_doc_type):
    print(doc_type)
    document_type = doc_type.objects.values_list('type', flat=True)
    print("--------------", document_type)
    if new_doc_type not in document_type:
        print("-----insode---------", document_type)
        new = doc_type(
            type=new_doc_type
        )
        new.save()
        context = {
            'result': 'data added:  ' + str(new_doc_type)
        }
    else:
        context = {
            'result': 'duplicate data:  ' + str(new_doc_type)
        }

    print("addd doc")
    return JsonResponse(context, safe=False)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def rag_for_docma(requests):
    print("---------Rag data  for Docma --------------------------------------")
    q1 = docma.objects.all()
    data = list(docma_firebase.objects.values())
    return JsonResponse(data, safe=False)


def home_menu_req():
    # document_type = doc_type.objects.values_list('type', flat=True)
    menu_but = home_menu.objects.all().order_by('app_priority')
    return menu_but

### ------------ check here ------------ ###


def give_path():
    random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
    if os.path.exists('AURA_MK2/cloud'):
        upload_dir = 'AURA_MK2/buffer/'+random_code+'/'
        main_folder = 'AllDocuments/'
    else:
        upload_dir = 'assets/buffer/'+random_code+'/'
        main_folder = 'Test/'

    if not os.path.exists(upload_dir): os.makedirs(upload_dir)
    return upload_dir, main_folder


def doc_manager_save_firebase(request):
    if request.method == 'POST':

        docName = request.POST['docName']
        docType = request.POST['docType']
        refNum = request.POST['refNum']
        sDate = request.POST['sDate']
        eDate = request.POST['eDate']
        remarks = request.POST['remarks']
        value = request.POST['value']



        local_dir , firebase_folder = give_path()

        # if os.path.exists('AURA_MK2/assets/cloud'):
        #     upload_dir = 'AURA_MK2/assets/buffer/'+random_code+'/'
        #     main_folder = 'Docmanger/'
        # else:
        #     upload_dir = 'assets/buffer/'+random_code+'/'
        #     main_folder = 'Test/'


        firebase_storage_path = firebase_folder + docType + '/' + refNum + '_' + docName + '/'
        files_data = ''
        for file in request.FILES.getlist('file'):
            with open(local_dir +str(file), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            bucket.child(firebase_storage_path + str(file)).put(local_dir + str(file))
            files_data = files_data  + str(file) + '|'
        shutil.rmtree(local_dir)
        enc_value = ''
        if docType == 'Bank_Cards':
            enc_value = encrypt_value(value)
        else:
            enc_value = value

        data = docma_firebase(holder=docName,
                              refnumber=refNum,
                              document_path=firebase_storage_path,
                              document_list = files_data,
                              end_date=eDate,
                              start_date=sDate,
                              value=enc_value,
                              type=docType,
                              time_stamp=datetime.now(),
                              remarks=remarks,
                              updated_by=request.user.username
                              )
        data.save()


    return add_document(request)
    # return render(request, "DocManager_form.html")


def doc_viewer_firebase(request, type):
    document_data = docma_firebase.objects.filter(type=type)
    viewer = {}
    for document in document_data:
        path = []
        print(document.holder, document.refnumber, document.end_date)
        print(document.document_list)
        for file in document.document_list.split('|'):
            if file != '':
                print(document.document_path+file)
                path.append(bucket.child(document.document_path+file).get_url(None))

        viewer[str(document.holder) + str(document.id)] = {
            'doc_id': document.id,
            'refnum': document.refnumber,
            'valid': document.end_date,
            'file_path': path,}

    document_holders = doc_holder.objects.values_list('Holder', flat=True)
    document_type = doc_type.objects.values_list('type', flat=True)



    context = {
        'document_holders': document_holders,
        'document_type': document_type,
        'data': viewer

    }

    print(viewer)

    return render(request, "Docma_DocumentViewer.html", context)

def get_data_by_id_firebase(request, id):
    q1 = docma_firebase.objects.filter(id=id)


    data = {
        'id': q1[0].id,
        'name': q1[0].holder,
        'type': q1[0].type,
        'ref': q1[0].refnumber,
        'sdate': q1[0].start_date,
        'edate': q1[0].end_date,
        'value': q1[0].value,
        'remarks': q1[0].remarks
    }

    return JsonResponse(data, safe=False)

def add_edit_document_firebase(requests):
    edited_data = json.loads(requests.body)
    print(edited_data , "Requested Edit data ")
    data_id_instance = docma_firebase.objects.filter(id=edited_data['id'])

    local_dir, firebase_folder = give_path()
    enc_value = encrypt_value(edited_data['value']) if edited_data['type'] == 'Bank_Cards'  else edited_data['value']
    for i in data_id_instance:
        old_data = {
        'ref_num' : i.refnumber,
        'type' : i.type,
        'holder' : i.holder,
        'document_list' : i.document_list
        }

    # dwnld to buffer
    cloud_des_path = f"{firebase_folder}{edited_data['type']}/{edited_data['ref'] + '_' + edited_data['name']}/"
    print(local_dir)
    for doc in old_data['document_list'].split('|'):
        if doc != '':
            cloud_source_path = f"{firebase_folder}{old_data['type']}/{old_data['ref_num'] + '_' + old_data['holder']}/{doc}"
            # print(cloud_source_path , "----------")
            print(cloud_source_path +'|'+ local_dir +'|'+doc , "------------")
            # bucket.child('Test/Passport/156_Panisha/loading.gif').download('/', 'hi.gif')
            bucket.child(cloud_source_path).download( '' , local_dir+ doc)
            bucket.child(cloud_des_path + doc).put(local_dir + doc)

    data_id_instance.update(
        holder=edited_data['name'],
        refnumber=edited_data['ref'],
        document_path = cloud_des_path,
        end_date=edited_data['edate'],
        start_date=edited_data['sdate'],
        value=enc_value,
        type=edited_data['type'],
        time_stamp=datetime.now(),
        remarks=edited_data['remarks'],
        updated_by=requests.user.username
    )

    shutil.rmtree(local_dir)

    return JsonResponse({'status': 'True'}, safe=False)

