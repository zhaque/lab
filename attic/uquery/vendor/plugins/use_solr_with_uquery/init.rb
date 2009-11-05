require File.dirname(__FILE__) + '/lib/use_solr_with_uquery'

# Add plugin routes
require 'routing'
ActionController::Routing::RouteSet::Mapper.send :include, UseSolrWithUquery::Routing::MapperExtensions

# Add plugin models, controllers and helpers paths
%w{ models controllers helpers }.each do |dir|
  path = File.join(File.dirname(__FILE__), 'lib/app', dir)
  $LOAD_PATH << path
  ActiveSupport::Dependencies.load_paths << path
  ActiveSupport::Dependencies.load_once_paths.delete(path)
end

# Add plugin views path
ActionController::Base.class_eval do
  append_view_path File.join(File.dirname(__FILE__), 'lib/app/views')
end

# Add application helpers

