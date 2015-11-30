from django.template import RequestContext, loader

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from SearchEngine import search_candidates

from jobseeker.models import Candidate


def delete_data_all():
    candidates = Candidate.objects.all()
    print candidates
    candidates.delete()
    print candidates
    users = User.objects.all()
    users.delete()


def search(request):
    search_dic = {}
    context = RequestContext(request, {
        'search_dic': search_dic
    })
    template = loader.get_template('talentseeker/search.html')
    return HttpResponse(template.render(context))


def search_submit(request):
    skills = request.POST['skills'].split(',')
    education = request.POST.getlist('education')
    experience = [request.POST['from'], request.POST['to']]

    si = search_candidates.SearchCandidates()
    result_list = si.search(skills, education, experience)
    request.session['result_list'] = result_list
    return HttpResponseRedirect(reverse('talentseeker:result'))


def result(request):
    result_list = request.session['result_list']
    template = loader.get_template('talentseeker/result.html')
    context = RequestContext(request, {
        'result_list': result_list
    })
    return HttpResponse(template.render(context))