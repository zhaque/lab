module UseSolrWithUquery
  module Routing
    module MapperExtensions
      def solr
        @set.add_route('/solr-tools/datas.json', {:controller => 'search_tools', :action => 'datas'})
        @set.add_route('/solr-tools/demo', {:controller => 'search_tools', :action => 'demo'})
      end
    end
  end
end