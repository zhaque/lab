# imports for side effects
import signal_handlers
from pipes import TwitterSearch
from user_profile import UserProfile

# register managed pipes
import mashup.pipeadmin
mashup.pipeadmin.register(TwitterSearch)
