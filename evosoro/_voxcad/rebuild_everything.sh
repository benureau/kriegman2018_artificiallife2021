#!/bin/bash

rm -Rf ~/include/voxelyze*
rm -Rf ~/lib/libvoxelyze*

qmake VoxCad.pro

echo "Cleaning and rebuilding current directory"
# make clean
make -j8

if [ $? -ne 0 ]; then
	echo "*** ERROR *** Cleaning and rebuilding current directory, quitting."
	exit 1
fi

echo "Cleaning, rebuilding and re-installing Voxelyze"
cd Voxelyze
make clean
make -j8
if [ $? -ne 0 ]; then
	echo "*** ERROR *** Cleaning and rebuilding Voxelyze, quitting."
	exit 1
fi
# make installusr

echo "Cleaning and rebuilding Voxelyze main"
cd ../voxelyzeMain/
make clean
make -j8

if [ $? -ne 0 ]; then
	echo "*** ERROR *** Cleaning and rebuilding Voxelyze main, quitting."
	exit 1
fi
echo "All done!"
