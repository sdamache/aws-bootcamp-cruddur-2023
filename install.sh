#!/bin/bash

set -e

## Install aws-cli
echo "Install aws-cli"
export AWS_CLI_AUTO_PROMPT=on-partial
cd /workspace
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
cd $THEIA_WORKSPACE_ROOT

## Install psql
echo "Install psql"
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
sudo apt update
sudo apt install -y postgresql-client-13 libpq-dev

## GITPOD_IP
echo "GITPOD_IP"
export GITPOD_IP=$(curl ifconfig.me)
source "$THEIA_WORKSPACE_ROOT/backend-flask/bin/rds-update-sgr-rule"



