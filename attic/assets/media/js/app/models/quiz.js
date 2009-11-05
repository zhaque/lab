/**
 * Example @VERSION - 
 *
 * Copyright (c) 2008-2009 ClayoolJS
 *
 */
(function($, $M){
    
    var cache;
	
    $M.Quiz = function(options){
		cache = {};
		return $.extend(true, this, options);
    };
	
	$.extend($M.Quiz.prototype,{
		get: function(id,callback){
			var _this = this;
			if (!cache[id]) {
				$.ajax({
					type: 'GET',
					url: 'http://assets.crowdsense.com/media/js/app/models/data/questions.json',
					dataType: 'json',
					success: function(json){
						_this.$log.debug('Succesfully retreived data');
						cache[id] = json;
						if (callback && $.isFunction(callback)) {
							callback(json);
						}
					}
				});
			}else{
				if (callback && $.isFunction(callback)) {
					callback(cache[id]);
   				}    
			}
		}
	});
    
    
})(jQuery,  Example.Models);
