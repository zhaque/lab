FLEXISOLR_OPTIONS = {
    'url': '/flexisolr/data.json',
    'url_server': '',
    'url_options': '&version=4',
    'pagination_area': 'pagination',
    'require_keyword': 1
}

FLEXISOLR_FILTERS = {
    'title': { 'field': 'title' },
    'summary': { 'field': 'summary_t' },
    'url': { 'field': '<a href="{url}">{url}</a>', 'type': 'custom' },
    'boost': { 'field': 'boost', 'default_value': '-' },
    'site_age': { 'field': 'site_age_l', 'default_value': '-' }
}

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


SOLR_CONFIG = {
    'solr': {
        'server_url': 'http://173.45.231.157/solr/select/'
        }
    }
