#!/bin/bash

#Copy between two buckets, inaccessible to each other

prof="lake-old"

path1=<path1>
path2=<path2>

tifs1=`aws s3 ls $path1 --profile $prof | grep tif | awk '{print $4}'`
tifs2=`aws s3 ls $path2 | grep tif | awk '{print $4}'`

#echo $tifs1
#echo $tifs2

for t1 in $tifs1; do
    flag=''
    name1=$(basename "$t1")
    for t2 in $tifs2; do
        name2=$(basename "$t2")
        if [ "$name1" = "$name2" ]; then
            #echo "YES $name1 exists -> skip";
            flag="EXISTS";
            break;
        fi
    done

    if [ -z $flag ]; then
        #echo "NO $name1 missing -> copy";
        echo "aws s3 cp $path1$name1 . --profile $prof"
        echo "aws s3 mv $name1 $path2"
    fi
done
