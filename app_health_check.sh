#!/usr/bin/bash

sleep 10
curl $(minikube ip):30007/1
check_var=$?

if [ $check_var -ne 0 ]
  then
    echo "Fail, health test NOT PASSED, application deploy, but not response"; exit 1
  else
    echo "Health test PASSED, application work fine "
fi
