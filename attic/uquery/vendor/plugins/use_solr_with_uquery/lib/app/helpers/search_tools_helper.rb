module SearchToolsHelper
  def include_jquery_javascript
    html = ''
    %w{
      jquery/jquery-1.2.6.min.js jquery/jquery.ui.all.min.js
      jquery/jquery.dimensions.min.js jquery/jquery.mousewheel.min.js
      jquery/jScrollPane.js jquery/chain-0.2.pack.js
    }.each do |js|
      html += javascript_include_tag js
    end
    html
  end
  
  def include_uquery_javascript
    html = ''
    %w{uquery/uquery uquery/search_engine}.each do |js|
      html += javascript_include_tag js
    end
    html
  end

  def include_jquery_stylesheets
    html = ''
    %w{jquery-ui/ui.all.css uquery/search_engine}.each do |css|
      html += stylesheet_link_tag css
    end
    html
  end

  def slide_in_out_block(name, facet)
    html =  '<div class="slide-in-out-block">'
    html <<   '<div class="slide-in-out-header">'
    html <<     "<span>#{name}</span>"
    html <<   '</div>'
    html <<   '<div class="slide-in-out-content">'
    html <<      facet
    html <<      '<br class="clear" />'
    html <<   '</div>'
    html << '</div>'
    html
  end

  def slider_facet(id)
    html = "<div id=\"#{id}\" class=\"ui-slider\"></div>"
    html += link_to 'reset', 'javascript:void(0);', :class => "reset #{id}_reset"
    html
  end
end