#!/bin/bash

# Check for Debian/Ubuntu-based systems
if [ -x "$(command -v apt-get)" ]; then
    echo "Detected Debian/Ubuntu-based system. Using 'apt' package manager."
    apt-get update
    apt-get install -y git awscli libspatialindex-dev tk bzip2 sudo locales fonts-liberation \
    gfortran g++ build-essential make wget openssh-client curl  gcc gcc-multilib \
    liblapack-dev libatlas-base-dev libblas-dev udunits-bin libudunits2-0 libudunits2-dev \
    libhdf5-dev libnetcdf-dev libnetcdff-dev netcdf-bin gdal-bin libgdal-dev libgeos-dev libproj-dev
    exit 0
fi

# If the script reaches this point, the distribution is not recognized
echo "Unsupported Linux distribution. Please install packages manually."
exit 1



