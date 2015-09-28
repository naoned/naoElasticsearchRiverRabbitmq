#!/bin/bash

DIR_TARGET="/opt/nao-elastic-river-rabbitmq/"

# Stop the dameon and delete service
/etc/init.d/nao-elastic-river-rabbitmq stop
sudo update-rc.d -f nao-elastic-river-rabbitmq remove
[ -f "/etc/init.d/nao-elastic-river-rabbitmq" ] && rm -f "/etc/init.d/nao-elastic-river-rabbitmq"

# Delete source files
[ -d "${DIR_TARGET}" ] && rm -rf ${DIR_TARGET}

# Delete /usr/bin program
[ -f "/usr/bin/nao-elastic-river-rabbitmq.sh" ] && rm -f "/usr/bin/nao-elastic-river-rabbitmq.sh"
