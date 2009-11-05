	$(function() {
		/*
		 * '+' tab dialog
		 */
		var search = $("#newtabquery"),
			allFields = $([]).add(search),
			tips = $("#validateTips");

		function updateTips(t) {
			tips.text(t).effect("highlight",{},1500);
		}

		/* check(): Display a validation tip if a condition fails.
		 * o: object field that is being checked.
		 * cond: condition that must be true to validate
		 * tip: text to show if !cond
		 */
		function check(o, cond, tip) {

			if ( !cond ) {
				o.addClass('ui-state-error');
				updateTips(tip);
				return false;
			} else {
				return true;
			}

		}


		var search_function = function() {
			var bValid = true;
			allFields.removeClass('ui-state-error');

			bValid = bValid && check(search, search.val().length > 0, "Please enter a search.");
			
			if (bValid) {
				// Create a new tab to the far right with the search results
				var $tabs = $("#tabs").tabs();
				var tab_count = $tabs.tabs('length');
				
				// We need to tell the results view that we are using =on for
				// services that are enabled and nothing for the others
				// so we pass this _formenabled, which is checked by the view.
				var url = '/app/results/?_formenabled=true&' + $("#newtabform").serialize();  //  + '?query=' + encodeURIComponent(search.val());
				
				$tabs.tabs('add', 
					url,  // anchor of the new tab. It must be unique or tabs break.
					search.val(),  // tab label
					tab_count - 1);  // Insert it before the "+"
				$tabs.tabs('select', tab_count - 1);

				$("#dialog").dialog('close');
			}
			
			return false; // necessary when we attach it to form submit
		};

		$("#newtabform").submit(search_function);

		$("#dialog").dialog({
			bgiframe: true,
			autoOpen: false,
			height: 400,
			modal: true,
			buttons: {
				'Search': search_function,
				Cancel: function() {
					$(this).dialog('close');
				}
			},
			close: function() {
				allFields.val('').removeClass('ui-state-error');
			}
		});
		
	});

	
	
	
	
	
	
	
	
	
	
	
	$(function() {
		/*
		 * Autocomplete
		 */
		$("#query").autocomplete(
			'/app/autocomplete/', // URL to autocomplete view
			{selectFirst: false}
		);
		
		
		

		/*
		 * All <a> inside the Trends tab must open in Results tab
		 */
		$('#tabs-1 a').click(function() {
			var 
			tab_count = $tabs.tabs('length');
			var url = this.href;
			$tabs.tabs('url', results_tab, url);
			$tabs.tabs('select', results_tab);

            return false;
        });


		var date_format = 'mm/dd/yyyy';
		var validate_date = function(date_input) {
			// TODO: Date validation
/*			try {
				debugger;
				var parsed = $.datepicker.parseDate(date_format, date_input.attr('value'));
				var formatted = $.datepicker.formatDate(date_format, parsed);
				date_input.attr('value', formatted);
			}
			catch(e) {
				date_input.attr('value', '');
			}
*/		
			return date_input.attr('value');
		};


		/*
		 * When the submit button on the search form is clicked, run search on Results tab
		 */
		var get_params;  // must remember the params when we submit a query so that then we can poll for new results using these same params
		function_submit = function() {
//			var url = '/app/results/?query=' + encodeURIComponent(query);  // DON'T use encode() - it doesn't handle Unicode


			validate_date($("#date_from"));
			validate_date($("#date_to"));
			get_params = $("#search-form").serialize();
			var url = "/app/results/?" + get_params;

			$.get(url, function(data) {
				$("#results").html(data);
			}, "html");

		    return false;
		};
		$('#querysubmit').click(function() {function_submit();});
		$('#search-form').submit(function(event) {
			event.preventDefault();
			function_submit();
		});



		/*
		 * Poll the server for new tweets.
		 */
		var poll_time = 10000;  // How frequently to poll the server for new tweets, in miliseconds
		var poll_function = function() {
			// The poll is with respect to this tab's query. #queryx is part of results.html
			var query = $("#queryx").html();
			
			if(query) {
				$.getJSON("/app/twitter/poll/?" + get_params,
					function(resp) {
						var newResults = resp['new'];
						
						if(newResults > 0) {
							$("#new-results").html("" + newResults 
								+ ' more results since you started searching. Click <a class="refresh" href="#">Refresh</a> to see them.');
							
							$(".refresh").click(function() {
								function_submit(query);  // Run the whole query again
							});
						}
						else
							$("#new-results").html("");
					}
				);
			}
			setTimeout(poll_function, poll_time);
		};
		setTimeout(poll_function, poll_time);
	});
	
	$(function() {
		/*
		 * Datepicker
		 */
		$("#date_from").datepicker();
		$("#date_to").datepicker();
		
	});
	