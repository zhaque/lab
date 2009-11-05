Flexisolr application
=====================

Configuration
-------------
Flexisolr application has it's own settings module (settings.py) which must be import ed in main settings module with line 

::

    from flexisolr.settings import *

There in flexisolr.settings are defined few variables. Configuration is set with it's values. They are explained below.

::

    FLEXISOLR_OPTIONS = {
        'url': '/flexisolr/data.json',
        'url_server': '',
        'url_options': '&version=4',
        'pagination_area': 'pagination',
        'require_keyword': 1
    }

General javascript options:

    - url: Url of your application which returns facets for JS, simply do not change;
    - url_server: hostname of server returning JSON (previous option), simply do not change;
    - url_options: options copied from ROR app;
    - pagination_area: id of html container where pagination is output;
    - require_keyword: 1 if search form requires some keyword, 0 if keyword is not required;

::

    FLEXISOLR_FACETS = (
        ('boost', {
            'type': 'double',
            'auto_request': False,
            'slider_min': 1,
            'slider_max': 9,
            'slider_min_text': '1',
            'slider_max_text': '10'
            }),
        ('site_age_l', {
            'type': 'double',
            'auto_request': False,
            })
        )



FLEXISOLR_FACETS holds definition of facets (after SOLR confiration).  It is a list of lists, each has facet field as it's first element and dictionary of options. Options have 'type' key mandatory and other obligatory. Type can be 'double', 'single' or 'list'. They call  uquery (solr-js) methods createDoubleSlider, createSingleSlider, createFiltersList. Options can be different, they depend on type, default are:

 - for 'double':

::

    {
          auto_request: true,
          value: 'middle',
          value_fixe: '',
          slider_min: '',
          slider_max: '',
          slider_min_text: '',
          slider_max_text: ''
        };

 - for single: 

::

    {
          auto_request: true,
          value_min: '',
          value_max: '',
          slider_min: '',
          slider_max: '',
          slider_min_text: '',
          slider_max_text: ''
        }

 - for list:

::

    {
          search_box: '',
          value: '*',
          filters: '',
          states: { },
          sort: false,
          custom_name: '{name}',
          custom_number: '{number}'
        }

Flexisolr does nothing with these values except that it generates Javascript code which performs uquery object calls. So for details of what options mean what refer to uquery.js.

::

    FLEXISOLR_FILTERS = {
        'title': { 'field': 'title' },
        'summary': { 'field': 'summary_t' },
        'url': { 'field': '<a href="{url}">{url}</a>', 'type': 'custom' },
        'boost': { 'field': 'boost', 'default_value': '-' },
        'site_age': { 'field': 'site_age_l', 'default_value': '-' }
    }

Filters definition is a dictionary. Each key is a name of filter. Each value is dictionary itself, can contain pairs with key name "field" (which is field) and key mame "title", which can be "custom" if "field" is not listed in it.

::

    SOLR_CONFIG = {
        'solr': {
            'server_url': 'http://173.45.231.157/solr/select/'
            }
        }

This is very important setting, the URL is /solr/select/ URL of your SOLR installation. Please keep in mind for GAE installation sthat GAE can fetch only from port 80 from other hosts.


Template tags
-------------

First you need to load template tags library: *{% load flexisolr %}* .
These two template tags must come first, they load required JS libraries and CSS files *{% include_jquery_js %}* and *{% include_jquery_css %}*.

Next, for each defined filter you should insert tag: *{% slide_in_out_block 'Page Authority' 'slider_boost' %}*
'Page Authority' is title of HTML block, and 'slider_boost' is name of filter in configuration data structure.
Name of field is created after name of field from dictionaries in FLEXISOLR_FILTERS.

Keyword input textfield and results along with paginator are output by this markup fragment:::

        <input type="text" name="keyword" id="keyword" />
        <input type="submit" id="submit-query" value="Run Report" />
        <br />
        <p class="results-informations">
          search results : <b class="results-count"></b>
          (display <b class="results-from"></b> to <b class="results-to"></b>)
        </p>
        <br />
        <div id="pagination" class="pagination"></div>
        <br />
        <div id="results">
          <div id="results-loader">
            <p>Please wait while loading data...</p>
          </div>
          <div id="results-empty">
            <p>No results.</p>
          </div>
          <div id="results-keyword-require">
            <p>Please enter a keyword.</p>
          </div>
          <div id="results-loop">
            <div class="result">
              <h1 class="title"></h1>
              <p class="summary"></p>
              <p>
                Page Authority :
                <span class="boost"></span> |
                Age of Site :
                <span class="site_age"></span>
                <br />
                <span class="url"></span>
              </p>
            </div>
          </div>
        </div>

After these tags, best - just before </body> tag, {% include_solr_js %}.

Example for 
-----------

I suppose you have set up Django project (or GAE Dango project) and have flexisolr app installed. Also, you have template file which gets rendered to browser successully, let it has name "template.html". I suppose you have facet "age of site" in your SOLR which field is called "site_age_l".


To have uquery up and running you have to edit configuration and edit template.html.

1) Edit configuration:

Assure flexisolr.settings contain code::

    FLEXISOLR_OPTIONS = {
        'url': '/flexisolr/data.json',
        'url_server': '',
        'url_options': '&version=4',
        'pagination_area': 'pagination',
        'require_keyword': 1
    }
    FLEXISOLR_FACETS = (
        ('site_age_l', {
            'type': 'double',
            'auto_request': False,
            })
        )
    FLEXISOLR_FILTERS = {
        'site_age': { 'field': 'site_age_l', 'default_value': '-' }
    }
    SOLR_CONFIG = {
        'solr': {
            'server_url': 'http://{whatever your hostname is}/solr/select/'
            }
        }

2) Edit template.html:
Insert code:::


        {% load flexisolr %}
        {% include_jquery_js %}
        {% include_jquery_css %}
        {% slide_in_out_block 'Age of Site' 'slider_site_age' %}
            <input type="text" name="keyword" id="keyword" />
            <input type="submit" id="submit-query" value="Run Report" />
            <br />
            <p class="results-informations">
              search results : <b class="results-count"></b>
              (display <b class="results-from"></b> to <b class="results-to"></b>)
            </p>
            <br />
            <div id="pagination" class="pagination"></div>
            <br />
            <div id="results">
              <div id="results-loader">
                <p>Please wait while loading data...</p>
              </div>
              <div id="results-empty">
                <p>No results.</p>
              </div>
              <div id="results-keyword-require">
                <p>Please enter a keyword.</p>
              </div>
              <div id="results-loop">
                <div class="result">
                  <h1 class="title"></h1>
                  <p class="summary"></p>
                  <p>
                    Page Authority :
                    <span class="boost"></span> |
                    Age of Site :
                    <span class="site_age"></span>
                    <br />
                    <span class="url"></span>
                  </p>
                </div>
              </div>
            </div>
        {% include_solr_js %}

This can be recombined, but keep in mind:
    a. {% load flexisolr %} goes first, before another your templates (not before extend tag if you use templates extending)
    b. {% include_jquery_js %} and {% include_jquery_css %} usually inserted into <head></head>
    c. {% slide_in_out_block 'Age of Site' 'slider_site_age' %} and big markup fragment must go after {% include_jquery_js %} and {% include_jquery_css %}
    d. {% include_solr_js %} must go after {% slide_in_out_block 'Age of Site' 'slider_site_age' %} and big markup fragment .

That's all, refresh page, get uquery working.

Installation of flexisolr 
-------------------------

Project I created is jsut a container project for flexisolr app. When you start use newer app-engine-patch or simply new Django project you have empty project skeleton. To use Flexisolr app with this new project you have to:

    1. Copy flexisolr folder into the project.
    2. Add 'flexisolr' into INSTALLED_APPS inside prokject's settings.py.
    3. Add ('^flexisolr/', include('flexisolr.urls')) to urls.py urlpatterns.
    4. Add line 'from flexisolr.settings import \*' to project's settigns.py.

After this you are able to use temnplate tags in your own templates.




