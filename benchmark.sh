#!/bin/bash

# -----------------------------------------------------------------------------
# Warm-up...
echo "Warm up..."
./benchmark.py -method none -linecount 0 -linetype segment -framecount 100

echo "None (1000 frames)"
./benchmark.py -method none -linecount 10000 -linetype segment -framecount 1000

echo "Raw (1000 frames)"
./benchmark.py -method raw -linecount 10000 -linetype segment -framecount 1000

echo "Solid (1000 frames)"
./benchmark.py -method solid -linecount 10000 -linetype segment -framecount 1000

echo "Dash solid (1000 frames)"
./benchmark.py -method dash-solid -linecount 10000 -linetype segment -framecount 1000

echo "Dash dotted (1000 frames)"
./benchmark.py -method dash-dotted -linecount 10000 -linetype segment -framecount 1000


# -----------------------------------------------------------------------------
# Warm-up...
echo "Warm up..."
./benchmark.py -method none -linecount 0 -linetype segment -framecount 1000

echo "Raw (0 to 1000 segments)"
for i in `seq 0 100 1000`
do
    ./benchmark.py -method raw -linecount $i -linetype segment -framecount 1000
done

echo "Solid (0 to 1000 segments)"
for i in `seq 0 100 1000`
do
    ./benchmark.py -method solid -linecount $i -linetype segment -framecount 1000
done

echo "Dash solid (0 to 1000 segments)"
for i in `seq 0 100 1000`
do
    ./benchmark.py -method dash-solid -linecount $i -linetype segment -framecount 1000
done

echo "Dash dotted (0 to 1000 segments)"
for i in `seq 0 100 1000`
do
    ./benchmark.py -method dash-dotted -linecount $i -linetype segment -framecount 1000
done


# -----------------------------------------------------------------------------
# Warm-up...
echo "Warm up..."
./benchmark.py -method none -linecount 0 -linetype segment -framecount 1000

echo "Raw (0 to 100 linewidth)"
for i in `seq 1 5 51`
do
    ./benchmark.py -method raw -linecount 1000 -linetype segment -framecount 1000 -linewidth $i
done

echo "Solid (0 to 100 linewidth)"
for i in `seq 1 5 51`
do
    ./benchmark.py -method solid -linecount 1000 -linetype segment -framecount 1000 -linewidth $i
done

echo "Dash solid (0 to 100 linewidth)"
for i in `seq 1 5 51`
do
    ./benchmark.py -method dash-solid -linecount 1000 -linetype segment -framecount 1000 -linewidth $i
done

echo "Dash dotted (0 to 100 linewidth)"
for i in `seq 1 5 51`
do
    ./benchmark.py -method dash-dotted -linecount 1000 -linetype segment -framecount 1000 -linewidth $i
done
