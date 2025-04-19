if [[ -z $1 ]]; then
    echo "usage ./version.generator <version number>"
    exit 1
fi

version="$1"

echo "Storing current stable version of the source at [ versions/$version ]"

find . -maxdepth 1 | while read f;
do
    f1=$(echo ${f} | awk -F/ '{print $2}')
    echo "Copying ${f1} -> versions/${version}"
    echo $f1
    if [[ "$f1" == "./TEST 1" ]]; then
        echo $f1
        exit 1
    fi
done
