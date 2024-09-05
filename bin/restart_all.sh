#!/bin/bash
# Force restart all services
docker compose pull
docker compose up -d --force-recreate