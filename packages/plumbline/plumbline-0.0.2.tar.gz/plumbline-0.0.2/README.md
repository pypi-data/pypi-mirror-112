# Plumbline

A unix filter script for whether or not a point cloud data source matches a known
benchmark DEM.


## Example

```
plumbline /vsicurl/https://hobu-lidar.s3.amazonaws.com/nasadem.vrt  \
    https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_MI_31Co_Jackson_2016_LAS_2019/ept.json \
    --sample_count 3 --plot jackson.pdf
```
