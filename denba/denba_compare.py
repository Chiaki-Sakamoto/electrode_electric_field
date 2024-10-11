from pylab import *
import numpy as np  # Numpy 環境を np として読み込み
# import scipy as sp # Scipy 環境を sp として読み込み
import matplotlib as mpl  # Matplotlib 環境を mpl として読み込み
import matplotlib.pyplot as plt
# Matplotlib.pyplot 環境を plt として読み込み　import matplotlib.cm as cm
import os.path
import matplotlib.font_manager as fm  # 図のフォント環境を定義
import matplotlib.gridspec as gridspec  # グリッド環境を定義
from matplotlib.ticker import *  # 目盛り環境
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.optimize import curve_fit
params = {
    "pdf.fonttype": 42  # PDF にフォント埋め込み
}
mpl.rcParams.update(params)  # 図のフォント環境の定義を Update

# from scipy.integrate import ode


def theory(x, z):
    rho_num = 1e-8*(1e-3**2)  # C/mm^2
    e0 = 8.85*1e-12*1e3  # 真空の誘電率 F/mm
    diameter = 1  # 電荷の半径 0.5mm
    dz = 0.1
    center = [int((len(z)-1)/2), int((len(x)-1)/2)]  # 計算領域の中央
    point_1 = (50, int(len(x)-1)/2)
    point_2 = (z[-1]-50, int(len(x)-1)/2)

    print(x.shape, z.shape, point_1, point_2, center)
    phi_theory = np.zeros((z.shape[0], x.shape[0]))

    x, z = np.meshgrid(x, z)
    A_1 = 1/(2*np.pi*e0)*rho_num*(np.pi*(diameter*dz)**2)
    A_2 = -A_1

    A_1 = rho_num*(diameter*dz)**2/(4*e0)
    A_2 = -A_1
    with np.errstate(divide='ignore'):  # withスコープ内のみ制御を適用する
        #        print((z-center[0]-(point_2[0]-center[0]))*dz)
        # +A_2/np.sqrt((((z-center[0])-(point_1[0]-center[0]))*dz)**2+((x-center[1])*dz)**2) # ３次元?
        phi_theory = 1 / \
            np.sqrt((((z-center[0])-(point_2[0]-center[0]))
                    * dz)**2+((x-center[1])*dz)**2)

        # phi_theory = np.log(1/np.sqrt((((z-center[0])-(point_2[0]-center[0]))*dz)**2+((x-center[1])*dz)**2))+1*np.log(1/np.sqrt((((z-center[0])-(point_1[0]-center[0]))*dz)**2+((x-center[1])*dz)**2))

        # phi_theory = np.log(1/np.sqrt(((z-center[0])-(point_2[0]-center[0]))**2+(x-center[1])**2))
    phi_theory = phi_theory.T

    return phi_theory


def theory_single(x, z):
    rho_e0 = 40 * 1e3  # 定数
    diameter = 5  # 電荷の半径 0.5mm
    delta = 1
    center = [int((len(z)-1)/2), int((len(x)-1)/2)]  # 計算領域の中央
    phi_theory = np.zeros((z.shape[0], x.shape[0]))
    x, z = np.meshgrid(x, z)
    A = rho_e0/(4*np.pi)
    with np.errstate(divide='ignore'):  # withスコープ内のみ制御を適用する
        phi_theory = A / \
            np.sqrt(((z-center[0])*delta*1e-3)**2 +
                    ((x-center[1])*delta*1e-3)**2)
        # phi_theory = np.log(1/np.sqrt((((z-center[0])-(point_2[0]-center[0]))*dz)**2+((x-center[1])*dz)**2))+1*np.log(1/np.sqrt((((z-center[0])-(point_1[0]-center[0]))*dz)**2+((x-center[1])*dz)**2))

        # phi_theory = np.log(1/np.sqrt(((z-center[0])-(point_2[0]-center[0]))**2+(x-center[1])**2))
    phi_theory = phi_theory.T
    print(phi_theory[200, 150])

    return phi_theory

####### 初期設定 #######
# phi= np.loadtxt("./denba_confirm/1015/dis300_re/phi.txt",delimiter = ",")
# Ez= np.loadtxt("./denba_confirm/1015/dis300_re/Ez.txt",delimiter = ",")
# Ex= np.loadtxt("./denba_confirm/1015/dis300_re/Ex.txt",delimiter = ",")

# phi_theory= np.loadtxt("./theory/Lx2000Lz2000/phi.txt",delimiter = ",")
# #Ez_theory= np.loadtxt("./theory/Lx2000Lz2000/Ez.txt",delimiter = ",")
# #Ex_theory= np.loadtxt("./theory/Lx2000Lz2000/Ex.txt",delimiter = ",")

# phi_theory= np.loadtxt("/Users/ichige/Desktop/charge_dis300/phi.txt",delimiter = ",")
# Ez_theory= np.loadtxt("/Users/ichige/Desktop/charge_dis300/Ez.txt",delimiter = ",")
# Ex_theory= np.loadtxt("/Users/ichige/Desktop/charge_dis300/Ex.txt",delimiter = ",")


Ez = np.loadtxt("./data/Ez.txt", delimiter=",")
Ex = np.loadtxt("./data/Ex.txt", delimiter=",")
x = np.arange(0, 201, 1)
z = np.arange(0, 201, 1)
fig, ax = plt.subplots(1, figsize=(7, 7))
im = plt.imshow(Ez, cmap="seismic")  # ,vmax = 1e-8,vmin = -1e-8)
streamplot(z, x, Ez, Ex, color='blue', broken_streamlines=False, density=0.3, zorder=0)
# ,t(z.shape[0])-1)/20)+1,10))
ax.tick_params(axis="both", width=1.5, size=20, labelsize=20, direction="in", top=True, right=True)  # 主目盛り．
ax.minorticks_on()
ax.tick_params(axis="both", which="minor", width=1.5, size=10, labelsize=20, direction="in", top=True, right=True)  # 副目盛り．

ax.set_xlabel("$z$ (mm)", size=24)  # 縦軸のタイトル
ax.set_ylabel("$x$ (mm)", size=24)  # 横軸のタイトル
# color bar #
cbar = fig.colorbar(im)
cbar.ax.tick_params(axis="y", labelsize=20, direction="in",
                    top="True", right="True", size=10)
cbar.ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
cbar.ax.minorticks_on()
cbar.ax.tick_params(axis="y", which="minor", direction="in", size=5)
# plt.clim(-40,40)
# plt.clim(-20,20)
cbar.set_label(label="Electrostatic field $E_\mathrm{z}$ (kV/cm)", size=24)
plt.savefig("./dipole.pdf")
plt.tight_layout()
plt.show()
