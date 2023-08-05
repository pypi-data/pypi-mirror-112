#!/bin/bash

cd "$(dirname $0)"

export ROOT=$(pwd)

if python -c "import sys; print(sys.version_info.major)" >& /dev/null;then
    export syspython=python
elif python3 -c "import sys; print(sys.version_info.major)" >& /dev/null;then
    export syspython=python3
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
