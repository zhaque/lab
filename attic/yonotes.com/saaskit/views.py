# Create your views here.

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from livesearch.models import SearchApi, AdvancedSearch
from muaccounts.models import MUAccount
from django.views.generic.simple import direct_to_template
from livesearch.forms import SearchesForm, AdvancedSearchForm


def save_apis(request):
    account = get_object_or_404(MUAccount, owner=request.user)
    search_apis = SearchApi.objects.all()
    if 'api_list' in request.POST:
        for api in search_apis:
          account.searchapis.remove(api)
        apis = request.POST.getlist('api_list')
        for api_id in apis:
          api_obj = SearchApi.objects.get(id=api_id)
          account.searchapis.add(api_obj)
        account.save()
    return HttpResponseRedirect(reverse('muaccounts_account_detail'))

def save_search_prefs(request):
    if request.method == "POST":
        account = get_object_or_404(MUAccount, owner=request.user)
        try:
            search_pref = AdvancedSearch.objects.get(muaccount = account)
        except ObjectDoesNotExist:
            search_pref = None
        
        form = AdvancedSearchForm(request.POST, request.FILES, instance=search_pref)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.muaccount = account
            obj.save()

    return HttpResponseRedirect(reverse('muaccounts_account_detail'))

def user_sites_index(request):
  search_apis = SearchApi.objects.all()
  for api in search_apis:
    if api.search_model != 'BingWeb':
        continue
    webapi = api
  form = SearchesForm()
  context_vars = {'api': webapi, 'form': form}
  return direct_to_template(request, template='user_sites/index.html', extra_context=context_vars)
