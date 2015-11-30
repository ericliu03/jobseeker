import json

from django.contrib.auth.models import User

from SearchEngine import search_candidates
from jobseeker.models import Candidate


def create_user(each_user):
    try:
        user = User.objects.create_user(username=each_user['email'], password=each_user['email'])
    except Exception as ex:
        print 'Error:', ex
        return

    candidate = Candidate.objects.create()
    for key, value in each_user.items():
        candidate.set_info(key, value)

    candidate.set_info('user_id', user.id)
    print user.id
    candidate.save()


def send_to_es():
    candidates = Candidate.objects.all()
    for_bulk_load = []
    for each in candidates:
        for_bulk_load.append(dict(each.get_profile_info()))
    print len(for_bulk_load)
    return for_bulk_load


def load_data(num=100):
    with open('SearchEngine/users.txt') as data_file:
        user_data = json.load(data_file)
        user_list = user_data['data'][:num]
    for each in user_list:
        create_user(each)

# uncomment next line to upload the data from file to website database
# load_data(1000)

# upload the data from website database to elasticsearch
si = search_candidates.SearchCandidates()
si.set_up_es(send_to_es())







