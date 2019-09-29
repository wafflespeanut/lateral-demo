#!/usr/bin/bash

REPO=~/assets

API_SERVE_DIR=~/app # NOTE: Changing this should also be reflected in the systemd unit.
NGINX_STATIC_DIR=/var/www/html
NGINX_CONFIG_DIR=/etc/nginx

export NVM_DIR="$HOME/.nvm"

# If `BOOTSTRAP` is set, then install one-time deps.
if [ ! -z "$BOOTSTRAP" ]; then
    apt install -y python3-pip \
        python3-dev \
        python3-venv \
        build-essential \
        libssl-dev \
        libffi-dev \
        nginx
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
    chmod +x $NVM_DIR/nvm.sh
fi

# Load nvm.
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install and set npm version if `BOOTSTRAP` is specified.
if [ ! -z "$BOOTSTRAP" ]; then
    nvm install --lts
fi

# Sync repo with Github.
if [ -d "$REPO" ]; then
    cd "$REPO" && git pull origin master
else
    git clone https://github.com/wafflespeanut/lateral-demo "$REPO"
    cd "$REPO"
fi

# Stop the service if it exists.
if [ $(systemctl is-active app.service) == 'active' ]; then
    systemctl stop app.service
fi

# Cleanup existing virtualenv.
rm -rf $API_SERVE_DIR
cp -r $REPO/server $API_SERVE_DIR
python3 -m venv $API_SERVE_DIR
source $API_SERVE_DIR/bin/activate
# Install packages.
pip3 install -r $API_SERVE_DIR/requirements.txt
deactivate

cp deploy/app.service /etc/systemd/system/
systemctl enable /etc/systemd/system/app.service
systemctl start app.service

# Build web app and forward static files to nginx.
cd web
npm install
npm run build

systemctl stop nginx
rm -rf $NGINX_STATIC_DIR && mv build $NGINX_STATIC_DIR

cp $REPO/deploy/nginx.conf   $NGINX_CONFIG_DIR/
cp $REPO/deploy/default.conf $NGINX_CONFIG_DIR/conf.d/
systemctl start nginx
