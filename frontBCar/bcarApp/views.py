from django.shortcuts import render,redirect
from django.http import FileResponse,HttpResponse
from django.views import View
from django.http import Http404
import os,asyncio,json,openpyxl
import pandas as pd
from bcarApp.givedata import main

class DownloadFileView(View):
    def get(self,request,*args,**kwargs):
        asyncio.run(main())
        with open("datas/data.json", "r") as json_file:
            data = json.load(json_file)

        df = pd.DataFrame.from_dict(data, orient='index')
        df.to_csv('datas/data.csv', index_label='ID')

        try:
            with open("datas/data.csv", "r", encoding="utf-8") as csv_file:
                data = pd.read_csv(csv_file)
        except UnicodeDecodeError:
            with open("datas/data.csv", "r", encoding="latin1") as csv_file:
                data = pd.read_csv(csv_file)

        data = data.drop(
            ["Description", "Address", "ID", "date", "Advantage_payment_amount"], axis=1
        )

        def convert_engine_capacity(capacity_str):
            try:
                return float(capacity_str.replace(" л", ""))
            except:
                return None

        def convert_mileage(mileage_str):
            try:
                mileage_parts = mileage_str.split(" ")
                return float(mileage_parts[0].replace(",", ""))
            except:
                return None

        data["Engine_capacity"] = data["Engine_capacity"].apply(convert_engine_capacity)
        data["Mileage"] = data["Mileage"].apply(convert_mileage)
        data["Mileage"] = data["Mileage"].fillna(value=0).astype(int)
        data["price"] = data["price"].fillna(value=0).astype(int)

        data.to_csv("datas/modified_data.csv", index=False, encoding='utf-8')
        data = pd.read_csv("datas/modified_data.csv", encoding='utf-8')
        data.to_excel("datas/modified_data.xlsx", index=False , engine='openpyxl')

        file_path = "datas/modified_data.xlsx"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        return render(request, 'index.html')


def index(request):
    global mlink
    if request.method == "POST":
        if request.POST.get("apartZ"):
            mlink ="https://www.unegui.mn/l-hdlh/l-hdlh-zarna/?page="
            print(mlink)
        if request.POST.get("apartT"):
            mlink ="https://www.unegui.mn/l-hdlh/l-hdlh-treesllne/?page="
            print(mlink)
        if request.POST.get("autoZ"):
            context = {
                'name': 'Авто машин зарна',
                'time': '5 минут',
            }
            mlink ="https://www.unegui.mn/avto-mashin/-avtomashin-zarna/?page="
            print(mlink)
        if request.POST.get("autoT"):
            context = {
                'name': 'Авто машин түрээслүүлнэ',
                'time': '3 минут',
            }
            mlink ="https://www.unegui.mn/avto-mashin/avto-treesllne/?page="
            print(mlink)
        return render(request,template_name='autoCar.html', context=context)
    return render(request,template_name = 'index.html')

def autoCar(request):
    if request.method == 'POST':
        value = request.POST.get("yes")
        if value == "yes":
            pass
        elif value == "no":
            return redirect('index')
    return render(template_name = 'autoCar.html', request = request)

def baby(request):
    return render(template_name = 'baby.html', request = request)

def clothing(request):
    return render(template_name = 'Clothing.html', request = request)

def immovable(request):
    return render(template_name = 'immovable.html', request = request)

def job(request):
    return render(template_name = 'job.html', request = request)

def animal(request):
    return render(template_name = 'animal.html', request = request)

def service(request):
    return render(template_name = 'service.html', request = request)

def electron(request):
    return render(template_name = 'electron.html', request = request)

def phone(request):
    return render(template_name = 'phone.html', request = request)

def Household(request):
    return render(template_name = 'Household.html', request = request)

def health(request):
    return render(template_name = 'health.html', request = request)

def computer(request):
    return render(template_name = 'computer.html', request = request)

def device(request):
    return render(template_name = 'device.html', request = request)
