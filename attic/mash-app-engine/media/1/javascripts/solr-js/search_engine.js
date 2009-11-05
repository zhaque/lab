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

// Function which append when search results finish
function addEvents() {
  if (solr.options.call == 2 && Boolean($('#keyword_default').val())) {
    $('#keyword').val($('#keyword_default').val());
    solr.onSearchEvent();
  }
}

flexisolr_options['callback'] = addEvents;

});

