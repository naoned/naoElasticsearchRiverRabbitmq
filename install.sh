#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
DIR_TARGET="/opt/nao-elastic-river-rabbitmq/"

# User who can interact with the dameon. In our case, the web server can control it
USER=naoriver
adduser --system $USER
addgroup --system $USER

# Installation of source files
echo ""
echo "Installation to ${DIR_TARGET} ..."
[ -d "${DIR_TARGET}" ] && rm -rf ${DIR_TARGET}
mkdir "${DIR_TARGET}"
cp -r "${DIR}"/* "${DIR_TARGET}"
[ -d "${DIR_TARGET}/log" ] && rm -rf "${DIR_TARGET}/log"
mkdir ${DIR_TARGET}/log
sudo chown -R $USER:$USER $DIR_TARGET
sudo chmod -R 775 $DIR_TARGET

# Creation of the service
echo "Create service..."
[ -f "/usr/bin/nao-elastic-river-rabbitmq.sh" ] && rm -f "/usr/bin/nao-elastic-river-rabbitmq.sh"
sudo ln -s "${DIR_TARGET}/daemon/nao-elastic-river-rabbitmq.sh" /usr/bin/nao-elastic-river-rabbitmq.sh
cp "${DIR_TARGET}/daemon/nao-elastic-river-rabbitmq" /etc/init.d/
chmod +x /etc/init.d/nao-elastic-river-rabbitmq
sudo update-rc.d nao-elastic-river-rabbitmq defaults 99

echo ""
echo "Done"
echo ""
