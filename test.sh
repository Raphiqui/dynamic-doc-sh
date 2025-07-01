#!/bin/bash

set -e

# @doc: Developer settings are used in development mode, don't use it if you deploy in production
# @default: YES
read -e -i yes -p "Use Developer Settings [YES/no]" sc3ui_pod_name_input
echo "Developer Settings: $sc3ui_pod_name_input"

# @doc: Pick the environment which meets your needs
# @default: dev
read -e -i staging -p "Select environment [staging/prod/dev]" environment
echo "Environment selected: $environment"

# @doc: k8s namespace must be specified otherwise none of the kubectl command will work
# @default: hello-world
read -e -i default -p "Enter Kubernetes namespace" namespace
echo "Namespace: $namespace"

# @doc: Pod name gives you access to a docker image
# @default: hello
read -e -i my-pod -p "Enter pod name" pod_name
echo "Pod Name: $pod_name"

# @doc: Container name
# @default: my-container
read -e -i app-container -p "Enter container name" container_name
echo "Container Name: $container_name"

echo "Running command: kubectl exec -n $namespace $pod_name -c $container_name -- echo Hello World"
