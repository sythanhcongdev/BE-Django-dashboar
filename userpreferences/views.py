from django.shortcuts import render
import os
import json
import pdb
from django.conf import settings
from .models import Userpreferences
from django.contrib import messages
# Create your views here.


def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        #k = key, v = value
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = Userpreferences.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = Userpreferences.objects.get(user=request.user)
    if request.method == 'GET':

        # check data import
        # pdb.set_trace()

        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
    else:
        currency = request.POST['currency']

        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            Userpreferences.objects.create(
                user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
