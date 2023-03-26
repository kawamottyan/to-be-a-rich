from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults

def predict(request):
    return render(request, 'predict.html')

def predict_chances(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        frame_number = float(request.POST.get('frame_number'))
        horse_number = float(request.POST.get('horse_number'))
        horse_weight = float(request.POST.get('horse_weight'))
        distance = float(request.POST.get('distance'))

        # Unpickle model
        model = pd.read_pickle('./keiba_model/model.pickle')
        # Make prediction
        result = model.predict([[frame_number, horse_number, horse_weight, distance]])

        rank = result[0]

        PredResults.objects.create(frame_number=frame_number, horse_number=horse_number, horse_weight=horse_weight,
                                   distance=distance, rank=rank)

        return JsonResponse({'result': rank, 'frame_number': frame_number,
                             'horse_number': horse_number, 'horse_weight': horse_weight, 'distance': distance},
                            safe=False)


def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)