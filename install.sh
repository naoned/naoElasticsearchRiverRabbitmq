#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
DIR_TARGET="/opt/nao-elastic-river-rabbitmq/"

echo ""
echo "Installation to ${DIR_TARGET} ..."
if [ -d "${DIR_TARGET}" ]; then
	rm -rf ${DIR_TARGET}
fi
mkdir "${DIR_TARGET}"
cp -r "${DIR}"/* "${DIR_TARGET}"

echo "Create service..."
if [ -f "/usr/bin/nao-elastic-river-rabbitmq.sh" ]; then
	rm -rf "/usr/bin/nao-elastic-river-rabbitmq.sh"
fi
sudo ln -s "${DIR_TARGET}/daemon/nao-elastic-river-rabbitmq.sh" /usr/bin/nao-elastic-river-rabbitmq.sh
cp "${DIR_TARGET}/daemon/nao-elastic-river-rabbitmq" /etc/init.d/
chmod +x /etc/init.d/nao-elastic-river-rabbitmq
sudo update-rc.d nao-elastic-river-rabbitmq defaults 99

echo ""
echo "done"
