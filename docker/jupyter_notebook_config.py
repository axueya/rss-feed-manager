import os
from IPython.lib import passwd

c = c  # pylint:disable=undefined-variable
c.NotebookApp.ip = '*'
c.NotebookApp.port = int(os.getenv('PORT', 8888))
c.NotebookApp.open_browser = False
c.NotebookApp.allow_remote_access = True

# sets a password if PASSWORD is set in the environment
c.NotebookApp.password = u'sha1:9f8094c6ef2c:1703a323786c820a554a93191bd5878d75e40526'
