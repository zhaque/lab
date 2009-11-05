$(document).ready(function() {

/**************************************************************************************
Slide in/out facets title
**************************************************************************************/

$('.slide-in-out-header').addClass('open');
$('.slide-in-out-header').click(function(){
  var content = $(this).parent().find('.slide-in-out-content');
  if (content.is(':hidden')) {
    content.slideDown();
    $(this).removeClass('close').addClass('open');
  } else {
    content.slideUp();
    $(this).removeClass('open').addClass('close')
  }
});


/**************************************************************************************
Add a scrollbar to the pane content (country list)
**************************************************************************************/

//$('#pane').jScrollPane();


/**************************************************************************************
Search engine
**************************************************************************************/

// Init fields list to get into results
var filters = {
  title: { field: 'title' },
  summary: { field: 'summary_t' },
  url: { field: '<a href="{url}">{url}</a>', type: 'custom' },
  boost: { field: 'boost', default_value: '-' },
  site_age: { field: 'site_age_l', default_value: '-' }
}

// Function which append when search results finish
function addEvents() {
  if (solr.options.call == 2 && Boolean($('#keyword_default').val())) {
    $('#keyword').val($('#keyword_default').val());
    solr.onSearchEvent();
  }
}

// Create search engine
var solr = new uQuery('solr', {
  //debug: true,
  url: '/solr-tools/datas.json',
  url_server: '',
  url_options: '&version=4',
  filters: filters,
  pagination_area: 'pagination',
  require_keyword: true,
  callback: addEvents
});

// boost (page rank) slider
solr.createDoubleSlider({
  field: 'boost',
  reset: 'slider_boost_reset',
  template: 'slider_boost',
  auto_request: false,
  slider_min: 1,
  slider_max: 9,
  slider_min_text: '1',
  slider_max_text: '10'
});

// site_age_facet slider
solr.createDoubleSlider({
  field: 'site_age_l',
  reset: 'slider_site_age_reset',
  template: 'slider_site_age',
  auto_request: false
});

// Execute uquery parsing
solr.render();

});