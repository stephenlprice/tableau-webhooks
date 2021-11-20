def when_ready(server):
    open('/tmp/app-initialized', 'w').close()

bind = 'unix:///tmp/nginx.socket'
