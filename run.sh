#!/bin/bash

# Launch our server, making it the process to ensure Docker behaves
# http://www.projectatomic.io/docs/docker-image-author-guidance/
cd /tmp
exec python3 tractdb_pyramid.py
