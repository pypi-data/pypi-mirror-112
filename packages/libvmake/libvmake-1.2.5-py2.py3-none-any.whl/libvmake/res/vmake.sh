#!/bin/bash

cd "$(dirname $0)"

export ROOT=$(pwd)

if python3 -c "import sys; sys.exit(0 if sys.version_info.major >= 3 else 1)" >& /dev/null;then
    export syspython=python3
elif python -c "import sys; sys.exit(0 if sys.version_info.major >= 3 else 1)" >& /dev/null;then
    export syspython=python
else
    echo "Error: no python3 found" >& 2
    exit 1
fi

if ! ${syspython} -c "import libvmake" 2> /dev/null;then
    ${syspython} -m pip install --no-input libvmake
fi

if [ ! -d "${ROOT}/.venv" ];then
    ${syspython} -m venv .venv
fi

${syspython} ./vmake.py $*
