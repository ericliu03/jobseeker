from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login, logout, get_user
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages

from .models import Candidate, HitHistory
from SearchEngine import jobsearch


def index(request, incurrect_up=None):
    template = loader.get_template('jobseeker/new_index.html')
    if incurrect_up:
        messages.error(request, 'The username or password you entered is incorrect.')
    context = RequestContext(request, {
        'messages': messages
    })
    return HttpResponse(template.render(context))


def login_prepare(request):
    post = request.POST

    user = authenticate(username=post['Username'], password=post['Password'])
    if user is not None:
        # the password verified for the user
        if user.is_active:
            login(request, user)
            candidate = Candidate.objects.get(user_id=user.id)
            return HttpResponseRedirect(reverse('jobseeker:search', args=(candidate.id,)))
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        # the authentication system was unable to verify the username and password
        return index(request, incurrect_up=True)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('jobseeker:index'))


def create_candidate(request, error=False):
    if error:
        messages.error(request, 'Username already exists')
    template = loader.get_template('jobseeker/new_candidate.html')
    candidate = Candidate.objects.get_or_create(user_id=0, name='model')
    context = RequestContext(request, {
        'candidate': candidate[0]
    })
    return HttpResponse(template.render(context))


def create_candidate_cancelled(request):
    return HttpResponseRedirect(reverse('jobseeker:index'))


def create_submit(request):
    try:
        user = User.objects.create_user(request.POST['Username'], password=request.POST['Password'])
    except Exception as ex:
        print ex
        return create_candidate(request, error=True)
    candidate = Candidate.objects.create()
    for key, value in request.POST.items():
        if key == 'Username' or key == 'Password':
            pass
        else:
            candidate.set_info(key, value)
    candidate.set_info('user_id', user.id)
    candidate.save()
    return HttpResponseRedirect(reverse('jobseeker:index'))


def edit_profile(request, pk):
    candidate_id = pk
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    if str(get_user(request).id) != candidate.user_id:
        return HttpResponseRedirect(reverse('jobseeker:index'))
    template = loader.get_template('jobseeker/edit_profile.html')
    context = RequestContext(request, {
        'candidate': candidate
    })
    return HttpResponse(template.render(context))


def edit_profile_submit(request, pk):
    candidate_id = pk
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    if str(get_user(request).id) != candidate.user_id:
        return HttpResponseRedirect(reverse('jobseeker:index'))

    for key, value in request.POST.items():
        candidate.set_info(key, value)
    candidate.save()
    return HttpResponseRedirect(reverse('jobseeker:search', args=(pk,)))


def search(request, pk):
    candidate_id = pk
    candidate = get_object_or_404(Candidate, pk=candidate_id)

    if str(get_user(request).id) != candidate.user_id:
        return HttpResponseRedirect(reverse('jobseeker:index'))

    temp = candidate.education.split()
    edu = {'phd': False, 'master': False, 'bachelor': False}
    for i in range(len(temp)):
        if temp[i] == 'phd':
            edu['phd'] = 1
        elif temp[i] == 'master':
            edu['master'] = 1
        elif temp[i] == 'bachelor':
            edu['bachelor'] = 1
    print edu
    template = loader.get_template('jobseeker/search.html')
    context = RequestContext(request, {
        'candidate': candidate,
        'edu': edu,
    })
    return HttpResponse(template.render(context))


def search_submit(request, pk):
    candidate_id = pk
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    print request.POST.items()
    for key, value in request.POST.items():
        if key == 'education':
            value = ','.join(request.POST.getlist('education'))
        elif key == 'skills':
            value = ','.join((request.POST.getlist('skills')))
        candidate.set_info(key, value)
    candidate.save()
    return HttpResponseRedirect(reverse('jobseeker:result', args=(candidate_id,)))


def result(request, pk):
    candidate_id = pk
    candidate = get_object_or_404(Candidate, pk=candidate_id)

    if str(get_user(request).id) != candidate.user_id:
        return HttpResponseRedirect(reverse('jobseeker:index'))

    hit_history_class = HitHistory.objects.filter(candidate=candidate)
    hit_history = [each.get_record() for each in hit_history_class]

    es = jobsearch.jobsearch()
    search_result, time_used = es.main_search(candidate.query_string, candidate.location,
                                              candidate.education.split(','),
                                              candidate.skills.split(','), candidate.job_type, candidate.company,
                                              candidate.search_range, candidate.use_history, hit_history)

    request.session['processed_result'] = search_result

    template = loader.get_template('jobseeker/result.html')
    context = RequestContext(request, {
        'result': search_result,
        'candidate': candidate,
    })
    return HttpResponse(template.render(context))


def job_detail(request, pk, counter):
    candidate_id = pk
    candidate = get_object_or_404(Candidate, pk=candidate_id)

    processed_result = request.session['processed_result'][int(counter) - 1]
    (hit_history, temp) = HitHistory.objects.get_or_create(candidate=candidate, job_id=processed_result['job_id'])

    hit_history.hits += 1
    hit_history.save()
    return redirect(processed_result['url'])