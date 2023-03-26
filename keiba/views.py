from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults

def predict(request):
    return render(request, 'predict.html')

def predict_chances(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        one = float(request.POST.get('one'))
        two = float(request.POST.get('two'))
        three = float(request.POST.get('three'))
        four = float(request.POST.get('four'))
        five = float(request.POST.get('five'))
        six = float(request.POST.get('six'))
        seven = float(request.POST.get('seven'))
        eight = float(request.POST.get('eight'))
        nine = float(request.POST.get('nine'))
        ten = float(request.POST.get('ten'))
        eleven = float(request.POST.get('eleven'))
        twelve = float(request.POST.get('twelve'))
        thirteen = float(request.POST.get('thirteen'))
        fourteen = float(request.POST.get('fourteen'))
        fifteen = float(request.POST.get('fifteen'))
        sixteen = float(request.POST.get('sixteen'))
        seventeen = float(request.POST.get('seventeen'))
        eighteen = float(request.POST.get('eighteen'))

        try:
            one = float(one)
            two = float(two)
            three = float(three)
            four = float(four)
            five = float(five)
            six = float(six)
        except ValueError:
            # 何か値が空白である場合は、再び予測ページを表示
            return render(request, 'keiba/base.html')
        
        today_race_X = pd.read_csv('./dataset/data/main/today.csv')
        today_race_X_withname = pd.read_csv('./dataset/data/main/today_withname.csv')

        today_race_X.loc[today_race_X['horse_number'] == 1, 'horse_weight'] = one
        today_race_X.loc[today_race_X['horse_number'] == 2, 'horse_weight'] = two
        today_race_X.loc[today_race_X['horse_number'] == 3, 'horse_weight'] = three
        today_race_X.loc[today_race_X['horse_number'] == 4, 'horse_weight'] = four
        today_race_X.loc[today_race_X['horse_number'] == 5, 'horse_weight'] = five
        today_race_X.loc[today_race_X['horse_number'] == 6, 'horse_weight'] = six
        today_race_X.loc[today_race_X['horse_number'] == 7, 'horse_weight'] = seven
        today_race_X.loc[today_race_X['horse_number'] == 8, 'horse_weight'] = eight
        today_race_X.loc[today_race_X['horse_number'] == 9, 'horse_weight'] = nine
        today_race_X.loc[today_race_X['horse_number'] == 10, 'horse_weight'] = ten
        today_race_X.loc[today_race_X['horse_number'] == 11, 'horse_weight'] = eleven
        today_race_X.loc[today_race_X['horse_number'] == 12, 'horse_weight'] = twelve
        today_race_X.loc[today_race_X['horse_number'] == 13, 'horse_weight'] = thirteen
        today_race_X.loc[today_race_X['horse_number'] == 14, 'horse_weight'] = fourteen
        today_race_X.loc[today_race_X['horse_number'] == 15, 'horse_weight'] = fifteen
        today_race_X.loc[today_race_X['horse_number'] == 16, 'horse_weight'] = sixteen
        today_race_X.loc[today_race_X['horse_number'] == 17, 'horse_weight'] = seventeen
        today_race_X.loc[today_race_X['horse_number'] == 18, 'horse_weight'] = eighteen

        today_race_X = today_race_X.sort_values('horse_number')
        train_baskets = today_race_X.groupby(["race_id"])["horse_id"].count().values
        X = today_race_X.drop(["race_id", "horse_id"], axis=1)
        
        model = pd.read_pickle('./dataset/model/model.pickle')
        
        y_pred = model.predict(X, group=train_baskets)

        # Unpickle model
        #model = pd.read_pickle('./dataset/model/model.pickle')
        # Make prediction
        #result = model.predict([[frame_number, horse_number, horse_weight, distance]])

        rank = y_pred[0]

        PredResults.objects.create(one=one, two=two, three=three, four=four, five=five,
                                   six=six, seven=seven, eight=eight, nine=nine, ten=ten,
                                   eleven=eleven, twelve=twelve, thirteen=thirteen, fourteen=fourteen, fifteen=fifteen,
                                   sixteen=sixteen, seventeen=seventeen, eighteen=eighteen, rank=rank)

        return JsonResponse({'result': rank, 'one': one, 'two': two, 'three': three, 'four': four, 'five': five,
                              'six': six, 'seven': seven, 'eight': eight, 'nine': nine, 'ten': ten,
                               'eleven': eleven, 'twelve': twelve, 'thirteen': thirteen, 'fourteen': fourteen, 'fifteen': fifteen,
                             'sixteen': sixteen, 'seventeen': seventeen, 'eighteen': eighteen},
                            safe=False)


def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)