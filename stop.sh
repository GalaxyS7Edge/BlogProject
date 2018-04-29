#!/usr/bin/env bash
# shut down uwsgi
uwsgi --stop /tmp/BlogProject.pid
# gracefully stop nginx
# sudo nginx -s quit