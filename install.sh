#!/bin/bash
command_exists() {
	command -v "$@" > /dev/null 2>&1
}

sh_c='sh -c'
if [ "$user" != 'root' ]; then
	if command_exists sudo; then
		sh_c='sudo -E sh -c'
	elif command_exists su; then
		sh_c='su -c'
	else
		cat >&2 <<-'EOF'
		Error: this installer needs the ability to run commands as root.
		We are unable to find either "sudo" or "su" available to make this happen.
		EOF
		exit 1
	fi
fi

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
$sh_c 'mkdir "${DIR_TARGET}"'
$sh_c 'cp -r "${DIR}"/* "${DIR_TARGET}"'
[ -d "${DIR_TARGET}/log" ] && rm -rf "${DIR_TARGET}/log"
$sh_c 'mkdir ${DIR_TARGET}/log'
$sh_c 'chown -R $USER:$USER $DIR_TARGET'
$sh_c 'chmod -R 775 $DIR_TARGET'

# Creation of the service
echo "Create service..."
[ -f "/usr/bin/nao-elastic-river-rabbitmq.sh" ] && rm -f "/usr/bin/nao-elastic-river-rabbitmq.sh"
$sh_c 'ln -s "${DIR_TARGET}/daemon/nao-elastic-river-rabbitmq.sh" /usr/bin/nao-elastic-river-rabbitmq.sh'
$sh_c 'cp "${DIR_TARGET}/daemon/nao-elastic-river-rabbitmq" /etc/init.d/'
$sh_c 'chmod +x /etc/init.d/nao-elastic-river-rabbitmq'
$sh_c 'update-rc.d nao-elastic-river-rabbitmq defaults 99'

echo ""
echo "Done"
echo ""
