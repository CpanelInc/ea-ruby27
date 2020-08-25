if defined?(Gem)
  require 'rubygems.rb'

  begin
    require 'abrt'
  rescue LoadError
  end
end
