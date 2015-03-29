#!/bin/bash

# Launch our server, making it the process to ensure Docker behaves
# http://www.projectatomic.io/docs/docker-image-author-guidance/
exec python3 /tmp/tractdb_pyramid.py
