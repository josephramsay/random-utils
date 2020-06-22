#!/bin/bash

#Fix broken metatdata with g_t

prof="lake-old"

path1=<path1>
path2=<path2>

tifs1=`aws s3 ls $path1 --profile $prof | grep tif | awk '{print $4}'`
#echo $tifs1
for t1 in $tifs1; do
    name1=$(basename "$t1")
    aws s3 cp $path1$name1 . --profile $prof
    gray=`gdalinfo -json $name1 | jq -r '[.bands[].colorInterpretation=="Gray"] | any'`
    echo "Found gray CI $gray"
    if [ "$gray" = "true" ]; then
        #reprocess the tiff and push it back
        fix=fix.$name1
        gdal_translate -of GTIFF -co PHOTOMETRIC=RGB -co COMPRESS=LZW $name1 $fix
	    mv $fix $name1
        #aws s3 mv $fix $path1 --profile $prof
	    #rm $name1
    fi
    aws s3 mv $name1 $path2
    #exit
done
