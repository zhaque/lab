(function($) { 

/*
 * uQuery (universal query).
 * uQuery allow you to display results according to your search engine.
 * Solr search engine is only the one on this 0.1 version.
 *
 * @namespace
 *
 * @alias jQuery.uQuery
 */ 	
uQuery = function(adapter, options) {
  this.init(adapter, options);
}

$.extend(uQuery.prototype, {
  /*
   * Version Number.
   *
   * @alias jQuery.uQuery.version
   * @property {String}
   */
  version: '0.1',
  
  /*
   * Search engine adapter.
   * Search engine adapter could be 'solr'
   *
   * @alias jQuery.uQuery.adapter
   * @property {String}
   */
  adapter: '',
  
  /*
   * myVar / other name.
   * Single or multiline description here.
   *
   * @alias jQuery.uQuery.myVar
   * @property {Array}
   *   @property {Integer}  call                     Calling counter (number of time where uQuery is called)
   *   @property {Boolean}  debug                    Enable or not debug
   *   @property {String}   url                      Url which will be call to get datas
   *   @property {String}   url_server               Url wchich will be give to 'url' to call search engine
   *   @property {String}   url_options              Params which will be added to the url
   *   @property {String}   keyword_id               Keyword field id
   *   @property {String}   keyword_value            Keyword value
   *   @property {Boolean}  require_keyword          Display results only if keyword is present
   *   @property {Integer}  results_per_page         The number of items per page
   *   @property {String}   results_per_page_id      HTML tag id where results per page nu,ber is present
   *   @property {Integer}  pagination_items         Maximum number of pagination entries that are visible
   *   @property {Integer}  current_page             The page which is selected when the pagination is initialized
   *   @property {Integer}  pagination_edge_items    Links always displayed to the begin and the end pagination toolbar
   *   @property {String}   pagination_link          Link target of the pagination links
   *   @property {String}   pagination_previous_text Text for the "Previous" link
   *   @property {String}   pagination_next_text     Text for the "Next" link
   *   @property {String}   pagination_ellipse_text  Text when there is a gap between the pagination numbers
   *   @property {Boolean}  pagination_previous_show Display or not the "Previous" link
   *   @property {Boolean}  pagination_next_show     Display or not the "Next" link
   *   @property {Array}    filters                  Results will be formater with this filters
   *   @property {String}   results_area             HTML id to display results
   *   @property {String}   pagination_area          HTML id to display pagination toolbar
   */
  options: {
    call: 0,
    debug: false,
    url: '',
    url_server: '',
    url_options: '',
    keyword_id: 'keyword',
    keyword_value: '',
    require_keyword: false,
    results_per_page: 10,
    results_per_page_id: '',
    pagination_items: 8,
    current_page: 0,
    pagination_edge_items: 2,
    pagination_link: 'javascript:void(0)',
    pagination_previous_text: 'Previous',
    pagination_next_text: 'Next',
    pagination_ellipse_text: '...',
    pagination_previous_show: true,
    pagination_next_show: true,
    filters: { },
    search_button_id: 'submit-query',
    results_area: 'results',
    results_loader_area: 'results-loader',
    results_empty_area: 'results-empty',
    results_loop_area: 'results-loop',
    results_keyword_require_area: 'results-keyword-require',
    results_informations_area: 'results-informations',
    pagination_area: '',
    callback: function(){ return false; }
  },

  /*
   * Search engine datas.
   * Datas from search engine are splited in this array.
   *
   * @alias jQuery.uQuery.datas
   * @property {Array}
   */
  datas: {
    count: 0,
    results: { },
    facets: { },
    stats: { }
  },
  
  /*
   * Facets.
   * List of facets which will be parsed and used to format search engine facets.
   *
   * @alias jQuery.uQuery.facets
   * @property {Array}
   */
  facets: { },

  /*
   * Temporarly html.
   * Html is saved when uQuery is inited and used with Chain.
   *
   * @alias jQuery.uQuery.temp
   * @property {Array}
   */
  temp: {
    results_loader: '',
    results_empty: '',
    results_loop: '',
    results_informations: '',
    facets: { }
  },

  /*
   * init.
   * Init uQuery options.
   *
   * @param {String}   adapter   Search engine adapter (solr)
   * @param {Array}    options   Options to display results, pagination etc.
   *
   * @alias jQuery.uQuery.init()
   */
  init: function(adapter, options) {
    // Security : keyword has to be empty on first call 
    if ((this.options.call == 0) && Boolean($('#'+ this.options.keyword_id).attr('value'))) {
      $('#'+ this.options.keyword_id).attr('value', '');
    }

    this.adapter = adapter;
    $.extend(this.options, options);
    
    this.saveHtmlElemets();
    this.setAjaxLoader();
  },
  
  /*
   * saveHtmlElemets.
   * Save html elements which will be used by Chain.
   *
   * @alias jQuery.uQuery.saveHtmlElemets()
   */
  saveHtmlElemets: function(){
    this.temp.results_loader = $('#'+ this.options.results_loader_area).html();
    this.temp.results_empty = $('#'+ this.options.results_empty_area).html();
    this.temp.results_loop = $('#'+ this.options.results_loop_area).html();
    this.temp.results_keyword_require = $('#'+ this.options.results_keyword_require_area).html();
    
    // Remove html from page
    $('#'+ this.options.results_area).html('');
    
    this.temp.results_informations = $('.'+ this.options.results_informations_area).html();
    
    // Remove html from page
    $('.'+ this.options.results_informations_area).html('');
  }, 
  
  /*
   * setAjaxLoader.
   * Set ajax loader (could be a picture, text etc.).
   *
   * @alias jQuery.uQuery.setAjaxLoader()
   */
  setAjaxLoader: function(){
    if (this.options.require_keyword && !Boolean($('#'+ this.options.keyword_id).attr('value'))) {
      $('#'+ this.options.results_area).html(this.temp.results_keyword_require);
    } else {
      $('#'+ this.options.results_area).html(this.temp.results_loader);
    }
  },

  /*
   * value_fixe : mean, middle, min, max, integer or empty
   *
   */
  createSingleSlider: function(options) {
    var default_options = {
      auto_request: true,
      value: 'middle',
      value_fixe: '',
      slider_min: '',
      slider_max: '',
      slider_min_text: '',
      slider_max_text: ''
    };
    
    this.createFacet($.extend(default_options, options, {'type': 'singleSlider'}));
  },

  createDoubleSlider: function(options) {
    var default_options = {
      auto_request: true,
      value_min: '',
      value_max: '',
      slider_min: '',
      slider_max: '',
      slider_min_text: '',
      slider_max_text: ''
    };
    
    this.createFacet($.extend(default_options, options, {'type': 'doubleSlider'}));
  },

  createFiltersList: function(options) {
    var default_options = {
      search_box: '',
      value: '*',
      filters: '',
      states: { },
      sort: false,
      custom_name: '{name}',
      custom_number: '{number}'
    };
    
    this.createFacet($.extend(default_options, options, {'type': 'list'}));
  },
  /*
   * createFacet.
   * Add a facet to the facets list.
   *
   * @param {Array}   facet               Facet options
   *   @param {String}   field            Facet field name
   *   @param {String}   type             Facet type, could be : 'list' (default) or 'slider'
   *   @param {String}   template         HTML template : have to be an ID
   *   @param {String}   reset            HTML reset link : have to be a CLASS
   *   @param {String}   search_box       HTML search box (input type text) : have to be an ID
   *   @param {String}   value            Selected value
   *   @param {Array}    filters          Custom filters
   *   @param {Array}    states           Selected filters
   *   @param {Boolean}  sort             Sort by number (true) or by name (false)
   *   @param {String}   custom_name      Customize the name value
   *   @param {String}   custom_number    Customize the number value
   *   @param {String}   value_min        Selected minimum value
   *   @param {String}   value_max        Selected maximum value
   *   @param {Integer}  slider_min       Slider minimum value (range)
   *   @param {Integer}  slider_max       Slider maximum value (range)
   *   @param {String}   slider_min_text  Slider left text
   *   @param {String}   slider_min_text  Slider right text
   *   
   * @alias jQuery.uQuery.createFacet()
   */
  createFacet: function(options) {
    // Add common options to facet configuration
    var default_options = {
      field: '',
      template: '',
      reset: '',
      disabled: false
    };
    
    // Save facet options
    this.facets[options.template] = $.extend(default_options, options);
    
    // Save html for Chain
    this.temp.facets[options.template] = $('#'+ options.template).html();
    
    // Remove html from page
    $('#'+ options.template).html('');
  },
  
  /*
   * render.
   * Init first loading datas :
   * - first call to get statistics
   * - second is to parse results according to current search
   *
   * @alias jQuery.uQuery.render()
   *
   * @see jQuery.uQuery.parse()
   */
  render: function() {
    var self = this;
    
    $.getJSON(self.options.url, { 
        url: self.buildServerUrl()
      },
      function (json) {
        // Save stats
        self.datas.stats = json.stats;
        
        // Increment calling counter
        self.options.call++;
        
        // Call function after finish everything
        self.parse('init');
      }
    );
  },
  
 /*
  * parse.
  * Create pagination bar, parse results/facets etc. according to actions :
  * - init (first loading results)
  * - paginate (onPageChange)
  * - filter (facet actions)
  *
  * @alias jQuery.uQuery.parse()
  *
  * @param {String}   type   Elements will be parsed according to action
  *
  * @see jQuery.uQuery.createBuilder()
  */  
  parse: function(type) {
    var self = this;
    
    $.getJSON(self.options.url, { 
        url: self.buildServerUrl()
      },
      function (json) {
        // Save datas
        self.datas.count = json.response.numFound;
        self.datas.results = json.response.docs;
        self.datas.facets = json.facet_counts;

        // Parse elements
        switch (type){
          case 'init':
            self.bindElements();
          case 'filter':
            self.parseFacets();
            if (self.options.require_keyword && !Boolean($('#'+ self.options.keyword_id).attr('value')))
              break;
            self.parsePagination();
          case 'paginate':
            self.parseResults();
            self.parseResultsInformations();
            break;
        }

        // Increment calling counter
        self.options.call++;
        
        // Call function after finish everything
        self.options.callback();
      }
    );
  },
  
  /*
   * bindElements.
   * Bind actions to elements on uQuery init.
   *
   * @alias jQuery.uQuery.bindElements()
   *
   * @see jQuery.uQuery.setAjaxLoader()
   * @see jQuery.uQuery.parse()
   */
  bindElements: function(){
    var self = this;

    // Add listener to 'textbox' keyword
    $('#'+ this.options.keyword_id).unbind().keypress(function (e) {
      if (e.which == 13) {
        self.onSearchEvent();
        return false;
      }
    });

    // Add listener to 'search' button
    $('#'+ this.options.search_button_id).unbind().click(function(){
      self.onSearchEvent();
      return false;
    });

    // Add listener to the results per page element
    if ($('#'+ this.options.results_per_page_id).length) {
      self.options.results_per_page = $('#'+ self.options.results_per_page_id).val();
      
      $('#'+ this.options.results_per_page_id).unbind().change(function(){
        self.setAjaxLoader();
        self.options.results_per_page = $('#'+ self.options.results_per_page_id).val();     
        self.parse('paginate');
      });
    }

    // Add listener to create a new object
    
    // Add delete function
    $('.create-object-submit').unbind().click(function(){
      
      alert('ser : '+ $('.create-object').serialize());
      return false;
      /*$.post(self.options.url_create, { object: $('.create-object').serialize() }, function(data){
        if (data == 'true') {
          self.setAjaxLoader();
          self.parse('filter');
        } else {

        }
      });*/
    });
  },
  
  /*
   * onSearchEvent.
   * Event on search (button, search box).
   *
   * @alias jQuery.uQuery.onSearchEvent()
   * @return {String/Array/Object/Integer/Boolean/Function}
   *
   * @see jQuery.uQuery.setAjaxLoader()
   * @see jQuery.uQuery.parse()
   */
  onSearchEvent: function() {
    if (this.options.require_keyword && !Boolean($('#'+ this.options.keyword_id).attr('value'))) {
      alert('Please enter a keyword.')
    } else {
      $('#ResultsColumn h1 strong').text($('#keyword').val())
      this.setAjaxLoader();
      this.options.current_page = 0;
      this.parse('filter');
    }
  },
  
  /*
   * parseFacets.
   * Loop on facets, format datas to display them according to type.
   *
   * @alias jQuery.uQuery.parseFacets()
   *
   * @see jQuery.uQuery.parseFacetTypeList()
   * @see jQuery.uQuery.parseFacetTypeSlider()
   */
  parseFacets: function() {
    var self = this;

    $.each(this.facets, function(key, facet){
      // List type
      if (facet.type == 'list'){
        // To switch between even/odd because results from solr are separate by comma
        var i = 0;
        // To increment datas
        var j = 0;
        // Facets values will be there
        var values = [];
        
        // Loop on custom filters
        if (Boolean(facet.filters)){
          $.each(facet.filters, function(filter, name){
            values[j] = {
              name: name,
              number: self.datas.facets.facet_queries[filter.replace('{keyword}', self.options.keyword_value)],
              filter: filter.replace('{keyword}', self.options.keyword_value)
            }
            j++;
          });
        } else {
          // Loop on current facet name to format filters
          $.each(self.datas.facets.facet_fields[facet.field], function(key, value){
            if (i == 0) {
              values[j] = {
                name: value,
                number: self.datas.facets.facet_fields[facet.field][key + 1]
              }
              j++;
            }
            i = i == 0 ? 1 : 0;
          });
        }
        self.parseFacetTypeList(facet, values);

      // Slider type single
      } else if ((facet.type == 'singleSlider') && (self.options.call == 1)) {
        if (!Boolean(facet.slider_min)) {
          facet.slider_min = self.datas.stats.stats_fields[facet.field].min;
        }
        if (!Boolean(facet.slider_max)) {
          facet.slider_max = self.datas.stats.stats_fields[facet.field].max;
        }
        self.parseFacetTypeSingleSlider(facet);
      // Slider type double
      }else if ((facet.type == 'doubleSlider') && (self.options.call == 1)) {
        if (!Boolean(facet.slider_min)) {
          facet.slider_min = self.datas.stats.stats_fields[facet.field].min;
        }
        if (!Boolean(facet.slider_max)) {
          facet.slider_max = self.datas.stats.stats_fields[facet.field].max;
          if (facet.slider_max == 4.9E-324) {
            facet.slider_max = facet.slider_min + 1;
          }
        }
        
        if (facet.slider_min == facet.slider_max) {
          alert(facet.slider_min + ' to ' + facet.slider_max);
          facet.slider_max = facet.slider_min + 1;
        }
        self.parseFacetTypeDoubleSlider(facet);
      }
    });
  },
  
  /*
   * parseFacetTypeList.
   * Display 'list' facet.
   * You can customize easily this type :
   * - simple list
   * - case to select
   * - checkbox like 
   * States of a filter event (on click) :
   * - 'none' (nothing append)
   * - 'select' (only results which belongs to the filter)
   * - 'exclude' (only results which don't belongs to the filter(s))
   * - 'revert' (to revert an 'select' or 'exclude' event)
   * A filter is also 'disabled' if data number is empty
   *
   * @param {Array}   facet   Facet to use
   * @param {Array}   values  Values to parse
   *
   * @alias jQuery.uQuery.parseFacetTypeList()
   *
   * @see jQuery.uQuery.onFacetEvent()
   */
  parseFacetTypeList: function(facet, values){
    var self = this;
    
    $('#'+ facet.template)
      .html(this.temp.facets[facet.template])
      .items(values)
      .chain({
        '.name': facet.custom_name,
        '.number': facet.custom_number,
        '.linked_to_default': function(data, el){
          el.click(function(){
            var states = {};
            $.each(self.facets[facet.template].states, function(name, state) {
              if (name != (Boolean(data.filter) ? data.filter : data.name)) {
                states[name] = state;
              }
            });
            self.facets[facet.template].states = states;
            self.onFacetEvent();
          });
        },
        '.linked_to_select': function(data, el){
          el.click(function(){
            var states = {};
            $.each(self.facets[facet.template].states, function(name, state) {
              if (state != 'excluded') {
                states[name] = state;
              }
            });
            self.facets[facet.template].states = states;
            self.facets[facet.template].states[Boolean(data.filter) ? data.filter : data.name] = 'selected';
            self.onFacetEvent();
          });
        },
        '.linked_to_exclude': function(data, el){
          el.click(function(){
            self.facets[facet.template].states[Boolean(data.filter) ? data.filter : data.name] = 'excluded';
            self.onFacetEvent();
          });
        },
        'builder': function(root){
          var name = Boolean(this.item()['filter']) ? this.item()['filter'] : this.item()['name']

          // Display only 'disabled'
          if (this.item()['number'] == 0 && !Boolean(self.facets[facet.template].states[name])) {
            this.find('.disabled').show();
          // Display only 'event'
          } else if (Boolean(self.facets[facet.template].states[name])) {
            this.find('.'+ self.facets[facet.template].states[name]).show();
          // Display only 'default'
          } else {
            this.find('.default').show();
          }
        }
      });
    
    // Add filter box
    if (Boolean(facet.search_box)) {
      $('#'+ facet.search_box).unbind().keyup(function(){
        $('#'+ facet.template).items('filter', $(this).val());
      });
    }

    // Reset values
    if (Boolean(facet.reset)) {
      $('.'+ facet.reset).unbind().click(function(){
        self.facets[facet.template].states = { };
        self.onFacetEvent();
      });
    }
  },
  
  /*
   * parseFacetTypeDoubleSlider.
   * Display 'slider' facet.
   *
   * @param {Array}   facet   Facet to use
   * @param {Array}   values  Values to parse
   *
   * @alias jQuery.uQuery.parseFacetTypeDoubleSlider()
   *
   * @see jQuery.uQuery.onFacetEvent()
   */
  parseFacetTypeDoubleSlider: function(facet, values){
    var self = this;
    
    $('#'+ facet.template).html(''
      + '<div class="ui-slider-handle"></div>'
      + '<div class="ui-slider-handle"></div>'
      + '<span class="label-1"></span>'
      + '<span class="label-2"></span>');

    // Recover minimum and maximum slider values 
    var min = facet.slider_min;
    var max = facet.slider_max;
    
    $('#'+ facet.template + ' .label-1').text(Boolean(facet.slider_min_text) ? facet.slider_min_text : min);
    $('#'+ facet.template + ' .label-2').text(Boolean(facet.slider_max_text) ? facet.slider_max_text : max);

    $('#'+ facet.template).slider({
      stepping: 1,
      min: min,
      max: max,
      range: true,
      change: function(e, ui) {
        self.facets[facet.template].value_min = $('#'+ facet.template).slider('value', 0);
        self.facets[facet.template].value_max = $('#'+ facet.template).slider('value', 1);
        if (facet.auto_request) {
          self.onFacetEvent();
        }
      },
      handles: [
        {start: Boolean(facet.value_min) ? facet.value_min : min, min: min, max: max},
        {start: Boolean(facet.value_max) ? facet.value_max : max, min: min, max: max}
      ]
    });

    // Disable slider if minimum equal to maximum (can not slide)
    if (min == max) {
      $('#'+ facet.template +' .ui-slider-handle').hide();
      $('#'+ facet.template +' .label-2').hide();
      $('#'+ facet.template).slider('disable');
    }
    
    // Reset values
    if (Boolean(facet.reset)) {
      $('.'+ facet.reset).click(function(){
        self.facets[facet.template].value_min = '';
        self.facets[facet.template].value_max = '';
        $('#'+ facet.template).slider('moveTo', min, 0);
        $('#'+ facet.template).slider('moveTo', max, 1);
        self.onFacetEvent();
      });
    }
  },

  parseFacetTypeSingleSlider: function(facet, values){
    var self = this;
    
    $('#'+ facet.template).html(''
      + '<div class="ui-slider-handle"></div>'
      + '<span class="label-1"></span>'
      + '<span class="label-2"></span>');

    // Recover minimum and maximum slider values 
    var min = facet.slider_min;
    var max = facet.slider_max;

    $('#'+ facet.template + ' .label-1').text(Boolean(facet.slider_min_text) ? facet.slider_min_text : min);
    $('#'+ facet.template + ' .label-2').text(Boolean(facet.slider_max_text) ? facet.slider_max_text : max);
    
    $('#'+ facet.template).slider({
      stepping: 1,
      min: min,
      max: max,
      range: true,
      change: function(e, ui) {
        self.facets[facet.template].value = $('#'+ facet.template).slider('value', 0);
        if (facet.auto_request) {
          self.onFacetEvent();
        }
      },
      handles: [
        {start: Boolean(facet.value) ? facet.value : min, min: min, max: max}
      ]
    });

    // Disable slider if minimum equal to maximum (can not slide)
    if (min == max) {
      $('#'+ facet.template +' .ui-slider-handle').hide();
      $('#'+ facet.template +' .label-2').hide();
      $('#'+ facet.template).slider('disable');
    }
    
    // Reset values
    if (Boolean(facet.reset)) {
      $('.'+ facet.reset).click(function(){
        self.facets[facet.template].value = '';
        $('#'+ facet.template).slider('moveTo', min, 0);
        self.onFacetEvent();
      });
    }
  },
  
  /*
   * onFacetEvent.
   * Actions when user event on facet.
   *
   * @alias jQuery.uQuery.onFacetEvent()
   * 
   * @see jQuery.uQuery.setAjaxLoader()
   * @see jQuery.uQuery.parse()
   */
  onFacetEvent: function() {
    this.options.current_page = 0;
    this.setAjaxLoader();
    this.parse('filter');       
  },
  
  /*
   * parsePagination.
   * Create pagination toolbar.
   *
   * @alias jQuery.uQuery.parsePagination()
   */
  parsePagination: function(){
    var self = this;
    
    // Extract current_page from options
    var current_page = self.options.current_page;
    
    // Create a sane value for results_per_page
    self.options.results_per_page = (!self.options.results_per_page || self.options.results_per_page < 0) ? 1 : self.options.results_per_page;
    
    // Attach control functions to the DOM element 
    this.selectPage = function(page_id){ self.pageSelected(page_id);}
    this.prevPage = function(){ 
      if (self.options.current_page > 0) {
        self.pageSelected(current_page - 1);
        return true;
      }
      else {
        return false;
      }
    }
    this.nextPage = function(){ 
      if(self.options.current_page < numPages()-1) {
        self.pageSelected(self.options.current_page+1);
        return true;
      }
      else {
        return false;
      }
    }
    // When all initialisation is done, draw the links
    this.drawLinks();
  },

  /*
   * onPageChange.
   * Events after page change (display current pages, sentences etc.)
   *
   * @alias jQuery.uQuery.onPageChange()
   *
   * @see jQuery.uQuery.setAjaxLoader()
   * @see jQuery.uQuery.parse()
   */
  onPageChange: function(page){
    this.setAjaxLoader();
    this.options.current_page = page;
    this.parse('paginate');
  },

  /*
   * parseResults.
   * Parse results area.
   *
   * @alias jQuery.uQuery.parseResults()
   */
  parseResults: function(){
    if (this.datas.count == 0) {
      $('#'+ this.options.results_area).html(this.temp.results_empty);
    } else {
      var builder = this.createBuilder(this.options.filters);
      $('#'+ this.options.results_area).html(this.temp.results_loop);
      $('#'+ this.options.results_area).items(this.datas.results).chain(builder);
    }
  },
  
  /*
   * createBuilder.
   * Datas will be parsed according to filters to create a Chain builder.
   *
   * @alias jQuery.uQuery.createBuilder()
   */
  createBuilder: function(filters) {
    var self = this;
    
    // Filters which will be give to Chain object
    var builder = { };
    
    // Type 'multiple'
    var filters_multiple = { };
    
    // Loop on filters to format json
    $.each(filters, function(key, value) {
      if (value['type'] == 'multiple') {
        filters_multiple[key] = value;
      } else if (value['type'] == 'custom') {
        builder['.'+ key] = value['field'];
      } else if (value['type'] == 'limit') {
        builder['.'+ key] = function(data, el) {
          var string = data[value['field']][0];
          return string.substr(0, value['limit']);
        };
      } else if (value['type'] == undefined) {
        builder['.'+ key] = function(data, el) {
          if (data[value['field']] != '' && data[value['field']] != undefined) {
            return ''+ data[value['field']] +'';
          } else {
            return Boolean(value['default_value']) ? value['default_value'] : '';
          } 
        };
      }
    });

    var item_number = 1;
    
    // Custom Chain builder
    builder['builder'] = function(root){
      item = this;
      items = item.item();

      // Add even-odd classes
      this.addClass((item_number % 2 == 0) ? 'even' : 'odd');
      item_number++;
      
      // Loop on fields
      $.each(filters_multiple, function(key, value) {
        // If field exist on search engine results
        if (items[value['field']] != undefined) {
          // Multiple
          if (items[value['field']] != undefined && value['type'] == 'multiple') {
            field = { };
            field['.' + value['key']] = '{$data}';
            item.find('.'+ key).items(items[value['field']]).chain(field);
          } else {
            // Remove html element 
            item.find('.'+ key).remove();
          }
        }
      });
    }
    
    // Add delete function
    builder['.delete'] = function(data, el){
      el.click(function(){
        $.post(self.options.url_delete, { id: data['id'] }, function(data){
          if (data == 'true') {
            self.setAjaxLoader();
            self.parse('filter'); 
          } else {
            
          }
        });
      });
    }
    
    return builder;
  },
  
  /*
   * parseResultsInformations.
   * Parse sentence and replace keys by results informations.
   *
   * @example
   * <span class="results-from"></span> to <span class="results-to"></span>
   *
   * @alias jQuery.uQuery.parseResultsInformations()
   */
  parseResultsInformations: function() {
    var results_from = Boolean(this.datas.count) ? (this.options.current_page * this.options.results_per_page) + 1 : 0;
    var results_to = (this.options.current_page + 1) * this.options.results_per_page;
    results_to = this.datas.count > results_to ? results_to : this.datas.count;
    
    $('.'+ this.options.results_informations_area).html(this.temp.results_informations);
    $('.'+ this.options.results_informations_area).item({
      'results-from': Boolean(results_from) ? results_from : '0',
      'results-to': Boolean(results_to) ? results_to : '0',
      'results-count': Boolean(this.datas.count) ? this.datas.count : '0'
    }).chain();
  },
  
  /*
   * buildServerUrl.
   * Built url to call search engine (according to adapter).
   *
   * @alias jQuery.uQuery.buildServerUrl()
   * @return {String}
   */
  buildServerUrl: function(results_number) {
    var self = this;
    
    var url = self.options.url_server;
    
    // Add keyword
    self.options.keyword_value = Boolean($('#'+ self.options.keyword_id).attr('value')) ? $('#'+ self.options.keyword_id).attr('value') : '*:*';
    url += '?q='+ self.options.keyword_value;

    // Paginate results
    if (results_number == undefined) {
      url += '&rows='+ self.options.results_per_page;
      url += '&start='+ self.options.current_page * self.options.results_per_page;
    } else {
      url += '&rows='+ results_number + '&start=0';
    }

    // Add facets and filters from facets
    if (self.facets != undefined) {
      
      // Init : need only statistics
      if (self.options.call == 0) {
        // Init default faceting attributes
        url += '&stats=true';

        $.each(self.facets, function(key, facet) {
          switch (facet.type){
            case 'singleSlider': 
              url += '&stats.field='+ facet.field;
              break;
            case 'doubleSlider':
              url += !Boolean(facet.slider_min) && !Boolean(facet.slider_max) ? '&stats.field='+ facet.field : '';
              break;
          }
        });
      // All other requests
      } else {
        // Init default faceting attributes
        url += '&facet=true&facet.sort=false&facet.mincount=0';

        $.each(self.facets, function(key, facet) {
          if (Boolean(facet.filters)) {
            // Add custom filters
            $.each(facet.filters, function(filter, name) {
              url += '&facet.query='+ filter.replace('{keyword}', self.options.keyword_value);
            });
          } else if (facet.type == 'list') {
            // Add current facet
            url += '&facet.field='+ facet.field;
            // Add facets results limit (10 first for example)
            url += '&f.'+ facet.field +'.facet.limit='+ (Boolean(facet.limit) ? facet.limit : '-1');
            // Add facets results minimum (display only if facet has one result minimum for example)
            url += Boolean(facet.mincount) ? '&f.'+ facet.field +'.facet.mincount='+ facet.mincount : '';
            // Sort facets by number (true) or by name (false)
            url += '&f.'+ facet.field +'.facet.sort='+ facet.sort;
          }

          if (!facet.disabled) {
            switch (facet.type){
              case 'list':
                // Init selected filters list
                var selected = new Array();

                $.each(facet.states, function(name, state) {
                  // Select expression separator
                  var separator = Boolean(facet.filters) ? '' : '\"';

                  // Select/exclude multiple or single filter(s)
                  switch (state) {
                    case 'selected':
                      selected[selected.length] = separator + name + separator;
                      break;
                    case 'excluded':
                      url += '&fq=-'+ facet.field +':'+ separator + name + separator;
                      break;
                  }
                });
                // Join selected filters
                if (Boolean(facet.filters)) {
                  url += (selected.length > 0) ? '&fq='+ selected.join('&fq=') : '';
                } else {
                  url += (selected.length > 0) ? '&fq='+ facet.field +':'+ selected.join('OR') : '';
                }
                break;
              case 'singleSlider':
                var stats = self.datas.stats.stats_fields[facet.field];

                switch (facet.value) {
                  case 'mean': facet.value = Math.round(stats.mean); break;
                  case 'middle': facet.value = Math.round((stats.min + stats.max) / 2); break;
                  case 'min': facet.value = Math.round(stats.min); break;
                  case 'max': facet.value = Math.round(stats.max); break;
                }
                switch (facet.value_fixe) {
                  case 'min': facet.value_fixe = Math.round(stats.min); break;
                  case 'max': facet.value_fixe = Math.round(stats.max); break;
                }

                // Single slider can use 2 types of ranges : value / value to value fixe (like double slider but only with one handler)
                url += Boolean(facet.value) && Boolean(facet.value_fixe) ? '&fq='+ facet.field +':['+ facet.value +'+TO+'+ facet.value_fixe +']' : '&fq='+ facet.field +':'+ facet.value;
                break;
              case 'doubleSlider':
                // Double slider use range values (something TO something)
                url += Boolean(facet.value_min) && Boolean(facet.value_min) ? '&fq='+ facet.field +':['+ facet.value_min +'+TO+'+ facet.value_max +']' : '';
                break;
            }
          }
        });
      }
    }

    // Format
    url += '&indent=on&wt=json';

    // Add url options
    url += self.options.url_options;

    // Debug
    if (self.options.debug) {
      $('body').prepend('<div id="debug">'+ url +'<div>');
    }
    
    // Return builded url
    return url;
  },
  
  /*
   * toString.
   * uQuery name and version.
   *
   * @alias jQuery.uQuery.toString()
   * @return {String}
   */
  toString: function() {
    return "uQuery (Javascript Universal Search Engine) v" + this.version;
  },
  
  /**
   * Calculate the maximum number of pages
   */
  numPages: function() {
    var count = (!this.datas.count || this.datas.count < 0) ? 1 : this.datas.count;
    return Math.ceil(count / this.options.results_per_page);
  },

  /**
   * Calculate start and end point of pagination links depending on
   * current_page and pagination_items.
   * @return {Array}
   */
  getInterval: function()  {
    var self = this;
    var ne_half = Math.ceil(self.options.pagination_items/2);
    var np = self.numPages();
    var upper_limit = np-self.options.pagination_items;
    var start = self.options.current_page>ne_half?Math.max(Math.min(self.options.current_page-ne_half, upper_limit), 0):0;
    var end = self.options.current_page>ne_half?Math.min(self.options.current_page+ne_half, np):Math.min(self.options.pagination_items, np);
    return [start,end];
  },

  /**
   * This is the event handling function for the pagination links.
   * @param {int} page_id The new page number
   */
  pageSelected: function(page_id, evt) {
    var continuePropagation = this.onPageChange(page_id);
    this.drawLinks();
    
    if (!continuePropagation) {
      if (evt.stopPropagation) {
        evt.stopPropagation();
      }
      else {
        evt.cancelBubble = true;
      }
    }
    return continuePropagation;
  },

  /**
   * This function inserts the pagination links into the container element
   */
  drawLinks: function() {
    var self = this;

    $('#'+ this.options.pagination_area).empty();
    var interval = self.getInterval();
    var np = self.numPages();

    if (np <= 1) return
    
    // This helper function returns a handler function that calls pageSelected with the right page_id
    var getClickHandler = function(page_id) {
      return function(evt){
        return self.pageSelected(page_id,evt);
      }
    }

    // Helper function for generating a single link (or a span tag if it'S the current page)
    var appendItem = function(page_id, appendopts) {
      var page_id = page_id<0?0:(page_id<np?page_id:np-1); // Normalize page id to sane value
      appendopts = jQuery.extend({text:page_id+1, classes:""}, appendopts||{});
      //alert(page_id +' == '+ self.options.current_page);
      if(page_id == self.options.current_page){
        var lnk = $("<span class='current'>"+(appendopts.text)+"</span>");
      }
      else
      {
        var lnk = $("<a>"+(appendopts.text)+"</a>")
                    .bind("click", getClickHandler(page_id))
                    .attr('href', self.options.pagination_link.replace(/__id__/,page_id));
      }
      if(appendopts.classes){lnk.addClass(appendopts.classes);}
      $('#'+ self.options.pagination_area).append(lnk);
    }
    // Generate "Previous"-Link
    if(self.options.pagination_previous_text && (self.options.current_page > 0 || self.options.pagination_previous_show)) {
      appendItem(self.options.current_page-1,{text:self.options.pagination_previous_text, classes:"prev"});
    }
    // Generate starting points
    if (interval[0] > 0 && self.options.pagination_edge_items > 0) {
      var end = Math.min(self.options.pagination_edge_items, interval[0]);
      for(var i=0; i<end; i++) {
        appendItem(i);
      }
      if(self.options.pagination_edge_items < interval[0] && self.options.pagination_ellipse_text) {
        jQuery("<span>"+self.options.pagination_ellipse_text+"</span>").appendTo($('#'+ self.options.pagination_area));
      }
    }
    // Generate interval links
    for(var i=interval[0]; i<interval[1]; i++) {
      appendItem(i);
    }
    // Generate ending points
    if (interval[1] < np && self.options.pagination_edge_items > 0)
    {
      if (np-self.options.pagination_edge_items > interval[1] && self.options.pagination_ellipse_text) {
        jQuery("<span>"+self.options.pagination_ellipse_text+"</span>").appendTo($('#'+ self.options.pagination_area));
      }
      var begin = Math.max(np-self.options.pagination_edge_items, interval[1]);
      for(var i=begin; i<np; i++) {
        appendItem(i);
      }

    }
    // Generate "Next"-Link
    if(self.options.pagination_next_text && (self.options.current_page < np-1 || self.options.pagination_next_show)){
      appendItem(self.options.current_page+1,{text:self.options.pagination_next_text, classes:"next"});
    }
  }
});

})(jQuery); 

  // Comments example

  /*
   * myVar / other name.
   * Single or multiline description here.
   *
   * @alias jQuery.uQuery.myVar
   * @property {String/Array/Object/Integer/Boolean/Function}
   *   @property {String/Array/Object/Integer/Boolean/Function}   param_name   Short description here
   */

  /*
   * myFunction.
   * Single or multiline description here.
   *
   * @param {String/Array/Object/Integer/Boolean/Function}   param_name   Short description here
   * @example
   * Single or multiline example here.
   *
   * @alias jQuery.uQuery.myFunction()
   * @return {String/Array/Object/Integer/Boolean/Function}
   *
   * @see @alias
   */