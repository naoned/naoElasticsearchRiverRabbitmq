#!/bin/bash

DIR_TARGET="/opt/nao-elastic-river-rabbitmq/"

# Stop the dameon and delete service
/etc/init.d/nao-elastic-river-rabbitmq stop
sudo update-rc.d -f nao-elastic-river-rabbitmq remove
if [ -f "/etc/init.d/nao-elastic-river-rabbitmq" ]; then
    rm -f "/etc/init.d/nao-elastic-river-rabbitmq"
fi

# Delete source files
if [ -d "${DIR_TARGET}" ]; then
	rm -rf ${DIR_TARGET}
fi

# Delete /usr/bin program
if [ -f "/usr/bin/nao-elastic-river-rabbitmq.sh" ]; then
	rm -f "/usr/bin/nao-elastic-river-rabbitmq.sh"
fi
