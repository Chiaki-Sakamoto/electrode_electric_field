set terminal pngcairo size 800,600
set output 'electric_field_vectors.png'
set title "2D Electric Field Vectors"
set xlabel "X-axis"
set ylabel "Y-axis"
unset zlabel
set noztics
unset zrange
set grid
set key off
set style data lines
set arrow from 0,0 to 1,0 nohead
set arrow from 0,0 to 0,1 nohead
set view 5, 30
splot '2d_Electric.csv' using 1:2:3 with pm3d, '' using 1:2:3:(1):(2) with vectors
