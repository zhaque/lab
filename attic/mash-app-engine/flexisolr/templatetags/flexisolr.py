from django import template
register = template.Library()

@register.inclusion_tag('flexisolr/templatetags/jquery_js.html', takes_context=True)
def include_jquery_js(context):
    context['list'] = [
        'jquery/jquery-1.2.6.min.js',
        'jquery/jquery.ui.all.min.js',
        'jquery/jquery.dimensions.min.js',
        'jquery/jquery.mousewheel.min.js',
        'jquery/jScrollPane.js',
        'jquery/chain-0.2.pack.js']
    return context

@register.inclusion_tag('flexisolr/templatetags/solr_js.html', takes_context=True)
def include_solr_js(context):
    context['list'] = [
        'solr-js/solr-js.js',
        'solr-js/search_engine.js']
    return context

@register.inclusion_tag('flexisolr/templatetags/jquery_css.html', takes_context=True)
def include_jquery_css(context):
    context['list'] = [
        'jquery-ui/ui.all.css',
        'uquery/search_engine.css']
    return context

@register.inclusion_tag('flexisolr/templatetags/slider_facet.html', takes_context=True)
def slider_facet(context, name):
    context['id'] = name
    return context

@register.inclusion_tag('flexisolr/templatetags/slide_in_out_block.html', takes_context=True)
def slide_in_out_block(context, name, facet):
    context.update({'name': name, 'facet': facet})
    return context

@register.inclusion_tag('flexisolr/templatetags/render_flexisolr.html', takes_context=True)
def render_flexisolr(context):
    return context

