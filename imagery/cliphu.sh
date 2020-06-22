#!/bin/bash

#simple transform

dir=$1
proj1=EPSG:3857
proj2=EPSG:4326
nodata=255

opt_lzw='COMPRESS=lzw'
opt_webp='COMPRESS=webp'
opt_thr='NUM_THREADS=ALL_CPUS'
opt_btf='BIGTIFF=YES'
opt_aa='ADD_ALPHA=YES'
opt_bs='BLOCKSIZE=512'
opt_rsp='RESAMPLING=bilinear'
opt_qty='QUALITY=90'
opt_sps='SPARSE_OK=YES'
opt_al='ALIGNED_LEVELS=6'

vrt_opts="-of VRT -wo $opt_thr"
cog_opts="-of COG -co $opt_webp -co $opt_thr -co $opt_btf -co $opt_aa -co $_bs-co $opt_rsp-co $opt_qty-co $opt_sps-co $opt_al"
tif_opts="-of GTiff -co $opt_lzw -co $opt_thr -co $opt_btf -co $opt_sps"

prof=lake-old

path1=s3://<path1>/
path2=s3://<path2>/
cutline=urban.geojson
tifs=`aws s3 ls $path1 --profile $prof | grep tif | cut -d' ' -f7`

for t in $tifs; do
    name=$(basename "$t" | cut -d. -f1)
    echo aws s3 cp $path1$t $dir --profile $prof
    echo gdalwarp -multi $vrt_opts -t_srs $proj1 -dstalpha -srcnodata $nodata -dstnodata $nodata -cutline $dir/$cutline -crop_to_cutline $dir/$t $dir/warp.$name.vrt
    echo gdal_translate $tif_opts $dir/warp.$name.vrt $dir/trans.$name.tif
    echo aws s3 cp $dir/trans.$name.tif $path2
    echo rm $dir/warp.$name.vrt
    echo rm $dir/trans.$name.tif
done
