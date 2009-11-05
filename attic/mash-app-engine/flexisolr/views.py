# -*- coding: utf-8 -*-
import urllib
import logging
from copy import deepcopy
from django.conf import settings
from django.utils import simplejson
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from google.appengine.api.urlfetch import fetch
from ragendja.template import render_to_response, render_to_string

def options(request):
    filters = deepcopy(settings.FLEXISOLR_FILTERS)
    options = deepcopy(settings.FLEXISOLR_OPTIONS)
    context = {
        'flexisolr_options': options
        }
    return render_to_response(request, 'flexisolr/options.js', context,
                              mimetype='application/javascript; charset=%s' % settings.DEFAULT_CHARSET)

def data(request):
    """
  def datas
    require 'open-uri'
    url = SOLR_CONFIG['solr']['server_url'] + params[:url]
    @datas = open(url.gsub(/\"/, "%22").gsub(" ", "%20"))
  end
  """
    SOLR_CONFIG = deepcopy(getattr(settings, 'SOLR_CONFIG', {}))
    try:
        url = SOLR_CONFIG['solr']['server_url']
    except KeyError:
        url = ''
    url += urllib.unquote(request.REQUEST.get('url', ''))
    response = fetch(url)
    return HttpResponse(response.content,
                        content_type='application/json; charset=%s' % settings.DEFAULT_CHARSET)
    
def render(request):
    filters = deepcopy(settings.FLEXISOLR_FILTERS)
    facets  = deepcopy(settings.FLEXISOLR_FACETS)
    controls = []
    for k, v in facets:
        logging.debug(v)
        for i, j in filters.items():
            if j['field'] == k:
                v['template'] = 'slider_' + i
                v['reset'] = v['template'] + '_reset'
                v['field'] = k
                t = v['type']
                del(v['type'])
                break
        controls.append((simplejson.dumps(v), deepcopy(t)))
    context = {
        'controls': controls
        }
    return render_to_response(request, 'flexisolr/render.js', context,
                              mimetype='application/javascript; charset=%s' % settings.DEFAULT_CHARSET)
