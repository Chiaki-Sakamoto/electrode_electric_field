import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

coords,ds = np.linspace(-0.6,0.6,100,retstep=True)


#XY領域の作成
X,Y = np.meshgrid(coords,coords)

k = 9.0*10**9
#微小区間の電荷の大きさ
q1=1

d=0.1
n=10000
#電極の範囲（長さ0.4の電極平板の作成）
x=np.linspace(-0.2,+0.2,n)
Z=0

for i in range(n):
  #電極の図示
  plt.plot(x[i],-d,'o',color='blue')
  plt.plot(x[i],d,'o',color='red')
  #電位の計算
  Z=Z-  k*q1/((X-x[i])**2+(Y+d)**2)**0.5+k*q1/((X-x[i])**2+(Y-d)**2)**0.5



n=100
#電位のグラフ 等高線n本
plt.contour(X,Y,Z,n)
plt.colorbar()


#勾配の配列は行方向、列方向の順で返されるので注意
#勾配つまり傾きを求める
dY,dX=np.gradient(Z,ds)
#電場
Ex=-dX
Ey=-dY

#電場のグラフ
plt.streamplot(X,Y,Ex,Ey)

# ax.quiver(X,Y,dX,dY)

plt.savefig("condenser.png")

plt.show()
