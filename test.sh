#!/bin/bash

set -e

sc3ui_pod_name="cmcc-sc3ui-0"
simulator_pod_name="cmcc-rsu-simulator-0"

# @doc: This is an example
echo "The default value for sc3ui pod name is $sc3ui_pod_name. Would you like to change it? (Press Enter to keep the default or type a new value)"
read sc3ui_pod_name_input

read -e -i yes -p "Use Developer Settings [YES/no]}" sc3ui_pod_name_input

echo "The default value for sc3ui pod name is $simulator_pod_name. Would you like to change it? (Press Enter to keep the default or type a new value)"
read simulator_pod_name_input

if [ -n "$simulator_pod_name_input" ]; then
  simulator_pod_name="$simulator_pod_name_input"
fi

echo "Now the values are $sc3ui_pod_name and $simulator_pod_name"
