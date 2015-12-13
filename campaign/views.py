from django.shortcuts import render
from pymongo import MongoClient
import pymongo
import random
from bson import ObjectId
from django.http import HttpResponseRedirect

client = MongoClient('localhost', 27017)
db = client.agency


def home(request):
    answer = db.imp_1.find().distinct("campaign_id")
    return render(request, 'banner/index.html', {'answer': answer})

def campaign(request, campaign_id):
    answer = db.statistics_1.find(
        {'campaign_id': int(campaign_id)},
        {'banner_id': 1, '_id': 0, 'total_revenue':1}
            ).sort([
                        ('total_revenue', -1),
                        ('total_clicks', -1)
                        ]).limit(10)
    board = []
    reserve = []
    for item in list(answer):
        if item['total_revenue'] > 0:
            board.append(item['banner_id'])
        else:
            reserve.append(item['banner_id'])
    if len(board) < 5:
        board.extend(reserve[0:(5-len(board))])
    answer = random.choice(board)
    if 'PreviouslySeen' in request.session and campaign_id in request.session['PreviouslySeen']:
        while answer in request.session['PreviouslySeen'][campaign_id]:
            board = [ b for b in board if b != answer]
            if len(board)==0 :
                break
            answer = random.choice(board)
        if len(board) > 0:
            request.session['PreviouslySeen'][campaign_id].append(answer)
            request.session.modified = True
        else:
            answer = 'Sorry... No more top banner to show.'
    else:
        request.session['PreviouslySeen']  = {}
        request.session['PreviouslySeen'] [campaign_id] = []
        request.session['PreviouslySeen'] [campaign_id].append(answer)
        request.session.modified = True
    return render(request, 'banner/campaign.html', {'answer': str(answer)})

def banner(request, campaign_id, banner_id):
    if request.method == 'POST':
        new_rev = int(request.POST['hour']) + float(request.POST['minute']) / 60
        print new_rev
        answer = db.statistics_1.update(
            {
                'campaign_id': int(campaign_id),
                'banner_id': int(banner_id)
            },
            {
                '$inc': {'total_revenue': new_rev}
            },)
        return HttpResponseRedirect('/campaign/%s/' % campaign_id)
    else:
        answer = db.statistics_1.find_one_and_update(
            {
                'campaign_id': int(campaign_id),
                'banner_id': int(banner_id)
            },
            {
                '$inc': {'total_clicks': 1}
            },)
    return render(request, 'banner/banner.html', answer)

