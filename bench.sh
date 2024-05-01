#!/bin/bash

TITLE() {
    echo -e "\n=== $*"
}

TITLE PREPARE
rm -rf go.* sample libc.c* build/ __pycache__/

MODNAME="sample"
go mod init $MODNAME
go mod tidy
go fmt ${MODNAME}.go
CGO_ENABLED=0 go build -trimpath -o $MODNAME
strip $MODNAME

python setup.py build_ext --inplace

TITLE GOLANG
echo "*** golang: single thread"
./sample 
echo -e "\n*** golang: multiple threads"
./sample -multicore

personObjs="Person PersonSlots PersonDataObject"
TITLE PYTHON
for obj in $personObjs ; do
    ./sample.py $obj
done

TITLE CYTHON
for obj in $personObjs ; do
    ./sample.py $obj libc
done

TITLE PYPY
for obj in $personObjs ; do
    pypy ./sample.py $obj
done

# grep -e ^= -e ^* | tr -d '\n' | \
# sed -e 's|\*\*\* |\n|g' -e 's|===|\n===|g' -e 's|* Total time:||g'
