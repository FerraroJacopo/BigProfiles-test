#!/usr/bin/env bash

real_script_path="$(realpath "$0")"
app_home="$(realpath "$(dirname "$real_script_path")")"

echo "$app_home"

docker-compose down --remove-orphans -v
