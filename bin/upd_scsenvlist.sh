#!/bin/sh

function help
{
cat <<EOF
Usage: ${0} <environment name>
Example ${0} skg
EOF
}

SCSENVLIST="${HOME}/scs/ScsEnvList"

if [ "${#}" != 1 ]; then
    echo "${0}: Incorrect number of parameters"
    help
    exit 1
fi

SCSENV="${1}"
shift

while (( "${#}" )); do
    echo ">> \${1} => ${1}"
    shift
done

if [ ! -f "${SCSENVLIST}" ]; then
    echo "${SCSENVLIST} does not exist"
    exit 1
fi

chmod +w "${SCSENVLIST}"
if [ $? != 0 ]; then
    echo "Failed to make ${SCSENVLIST} writable"
    exit 1
fi


sed -i -r -e "s/nel.{3}([12]a)/nel${SCSENV}\1/g" "${SCSENVLIST}"
if [ $? == 0 ]; then
    echo "${SCSENVLIST} has been updated successfully"
else
    echo "Failed to update ${SCSENVLIST}"
fi
