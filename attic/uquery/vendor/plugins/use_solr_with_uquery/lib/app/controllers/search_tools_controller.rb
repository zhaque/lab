class SearchToolsController < ActionController::Base
  def index
    render :text => 'Use Solr With uQuery plugin'
  end

  def datas
    require 'open-uri'
    url = SOLR_CONFIG['solr']['server_url'] + params[:url]
    @datas = open(url.gsub(/\"/, "%22").gsub(" ", "%20"))
  end
  
  def demo
   
  end
end