#!/bin/bash

if [[ $(curl http://${HOST}:${PORT} -w "%{http_code}\n" -s -o /dev/null) == "200" ]]
    echo "Application Started"
    exit 0
else
    echo "Waiting for application to start"
    exit 1
fi
