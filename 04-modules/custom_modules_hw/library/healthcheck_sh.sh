#!/bin/bash
# WANT_JSON

addr=$(cat $1 | grep -Po '(?<="addr": ")(.*?)(?=")')
tls=$(cat $1 | grep -Po '(?<="tls": )(.*?)(?=,)')

booleans=("y" "yes" "n" "no" "on" "off" "true" "false" "1" "0")
is_boolean=$(printf '%s\n' \"${booleans[@]}\" | grep -F -x "$tls")

if [[ ! $is_boolean ]]; then
    echo "{ \"failed\": true, \"site_status\": \"\", \"rc\": 1, \"msg\": \"TypeError: tls must has a boolean type\" }"
    exit 1
fi;

[[ $tls = "true" ]] && protocol="https" || protocol="http"

url="$protocol://$addr"
failed="false"
msg="Success"

response=$(curl -sI "$url" | head -n1)

rc=$(echo $response | cut -d ' ' -f 2)
site_status=$(echo $response | cut -d ' ' -f 3- | tr -d '\r')

if [[ $response = "" ]]; then
    rc=1
    failed="true"
    msg="ConnectionError. Can't connect to $url"
fi

echo "{ \"failed\": $failed, \"site_status\": \"$site_status\", \"rc\": $rc, \"msg\": \"$msg\" }"
