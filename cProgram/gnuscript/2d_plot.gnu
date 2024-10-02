set terminal pngcairo size 800,600
set output '2D_color_map.png'
set title "2D Potential Color Map"
set xlabel "X-axis"
set ylabel "Y-axis"
set cblabel "φ(x, y)"  # カラーバーのラベル
set pm3d map           # PM3Dを下に配置
set grid                # グリッドを表示
set palette defined ( 0 "blue", 1 "red" )  # カラーパレットを定義
splot '2d_Phi.csv' using 1:2:3 with pm3d
