$(document).ready(function() {
// Create search engine
var solr = new uQuery('solr', flexisolr_options);

{% for options, type in controls %}
{% ifequal type 'double' %}
solr.createDoubleSlider(
{% endifequal %}
{% ifequal type 'single' %}
solr.createSingleSlider(
{% endifequal %}
{% ifequal type 'list' %}
solr.createFiltersList(
{% endifequal %}
{% autoescape off %}
{{ options }}
{% endautoescape %}
);
{% endfor %}
// Execute uquery parsing
solr.render();

});
