#!/bin/bash

set -e

# @doc: Developer settings are used in development mode, don't use it if you deploy in production
# @default: yes
read -e -i yes -p "Use Developer Settings [YES/no]" developer_settings
echo "Developer Settings: $developer_settings"
