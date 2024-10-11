# 印加静電場分布をプロットするプログラム．
# 1.yamamoto.py で計算した印加静電場のtxtデータを読み込む．
# 2.電場分布のプロット
# 3.z軸上の電場
# 4.x軸上の電場

# (x,z) = (0,0) の配列要素は (x,z) = (200,150)
#############################################################################


import numpy as np  # Numpy 環境を np として読み込み
import scipy as sp  # Scipy 環境を sp として読み込み
import matplotlib as mpl  # Matplotlib 環境を mpl として読み込み
import matplotlib.pyplot as plt
# Matplotlib.pyplot 環境を plt として読み込み　import matplotlib.cm as cm
import os.path
import matplotlib.font_manager as fm  # 図のフォント環境を定義
import matplotlib.gridspec as gridspec  # グリッド環境を定義
from matplotlib.ticker import *  # 目盛り環境
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable
params = {
    "pdf.fonttype": 42  # PDF にフォント埋め込み
}
mpl.rcParams.update(params)  # 図のフォント環境の定義を Update

# ##yamamoto.pyから Ex,Ez の読みとり
# # #電極の穴の直径 15 mm の電場 Ez
# # Ez15 = np.loadtxt("/Users/ichige/Desktop/denba1/normal/10kV_13mm/Ey1.txt")*10
# # #電極の穴の直径 7.5 mm の電場 Ez
# # Ez75 = np.loadtxt("/Users/ichige/Desktop/denba1/normal/10kV_13mm/Ey1.txt")*10
# # #電極の穴の直径 15 mm の電場 Ex
# # Ex15 = np.loadtxt("/Users/ichige/Desktop/denba1/normal/10kV_13mm/Ex.txt")*10
# # #電極の穴の直径 7.5 mm の電場 Ex
# # Ex75 = np.loadtxt("/Users/ichige/Desktop/denba1/normal/10kV_13mm/Ex.txt")*10

# phi_5_13 = np.loadtxt("/Users/ichige/Desktop/keisan/a_m10kv/phi.txt",delimiter=",")
# phi_13_13 = np.loadtxt("/Users/ichige/Desktop/keisan/p_13mm_13mm/phi.txt",delimiter=",")

# print(phi_5_13.shape)
# x = np.arange(-150,151,1)
# y = np.arange(-200,201,1)
# Ez_5_13 = np.zeros((y.shape[0],x.shape[0]))
# Ex_5_13 = np.zeros((y.shape[0],x.shape[0]))
# Ez_13_13 = np.zeros((y.shape[0],x.shape[0]))
# Ex_13_13 = np.zeros((y.shape[0],x.shape[0]))

# for i in range(x.shape[0]):
#     for j in range(y.shape[0]):
#         if(x[0]<x[i]<x[-1]):
#             if(y[0]<y[j]<y[-1]):
#                 Ez_5_13[j,i] = (phi_5_13[j,i-1]-phi_5_13[j,i+1])/(2*0.1)
#                 Ex_5_13[j,i] = (phi_5_13[j-1,i]-phi_5_13[j+1,i])/(2*0.1)
#                 Ez_13_13[j,i] = (phi_13_13[j,i-1]-phi_13_13[j,i+1])/(2*0.1)
#                 Ex_13_13[j,i] = (phi_13_13[j-1,i]-phi_13_13[j+1,i])/(2*0.1)


# x_range = np.linspace(20, -20, Ex_5_13.shape[0])
# z_range = np.linspace(0,30,Ex_5_13.shape[1])

# line_x = 0 # [mm]
# mean_z = (10,20.1)

# #print(Ex75.shape)

# Ez_10 = np.loadtxt("/Users/ichige/Desktop/keisan/a_m10kv/Ex.txt",delimiter=",")
# ### 電場 Ez ###
# plt.figure(figsize=(12,9))
# plt.imshow((-Ez_5_13/100),cmap="Reds",vmin=0,vmax=20) #描写

# plt.yticks(np.arange(0,401,50), np.arange(-20,21,5)) #縦軸のメモリ間隔
# plt.xticks(np.arange(0,301,50),np.arange(-15,16,5))  #横軸のメモリ間隔
# plt.tick_params(axis="both",which="both",direction="in",
#         top=True,right=True,labelsize=35,width=1.7) #軸を内側にし文字の大きさ設定
# plt.ylim(49,351) #横軸の範囲指定
# plt.xlim(50,251) #縦軸の範囲指定
# plt.xlabel("z (mm)",size=50) #縦軸のタイトル
# plt.ylabel("x (mm)",size=50) #横軸のタイトル
# cbar = plt.colorbar() #カラーバー
# cbar.set_label('Electrostatic field Ez (kV/cm)',size=50) #カラーバーのタイトル
# #plt.savefig("/Users/ichige/Desktop/Ez_13_13.pdf",bbox_inches="tight")
# plt.close()


# ### 電場 Ex ###
# plt.figure(figsize=(12,9))
# plt.imshow((Ex_5_13/100),cmap="seismic",vmin=-20,vmax=20) #描写 Exはx軸正方向なので - をかける

# plt.yticks(np.arange(0,401,50), np.arange(-20,21,5)) #縦軸のメモリ間隔
# plt.xticks(np.arange(0,301,50),np.arange(-15,16,5))  #横軸のメモリ間隔
# plt.ylim(49,351) #縦軸の範囲指定
# plt.xlim(50,251) #横軸の範囲指定
# plt.tick_params(axis="both",which="both",direction="in",
#         top=True,right=True,labelsize=35,width=1.7) #軸を内側にし文字の大きさ設定
# plt.ylabel("x (mm)",size=50) #縦軸のタイトル
# plt.xlabel("z (mm)",size=50) #横軸のタイトル
# cbar = plt.colorbar() #カラーバー
# cbar.set_label('Electrostatic field Ex (kV/cm)',size=50) #カラーバーのタイトル
# #plt.savefig("/Users/ichige/Desktop/Ex_13_13.pdf",bbox_inches="tight")
# plt.close()
# #plt.show()

# ### z = 0 の電場強度分布 Ez ####
# plt.figure(figsize =(12,9))

# #電極の穴の直径 7.5 mm の強度分布
# plt.plot(np.arange(Ez_25.shape[0])/10-20,(-Ez_25[:,150]/1000),lw=5,color="r")
# #電極の穴の直径 15 mm の強度分布
# #plt.plot(np.arange(Ez15.shape[0])/10-20,(Ez15[:,150]*1e-3),lw=5,color="b",label = "15.0 mm")

# plt.yticks(np.arange(0,21,5),np.arange(0,21,5))     #縦軸のメモリ間隔
# plt.xticks(np.arange(-5,6,2.5),np.arange(-5,6,2.5)) #横軸のメモリ間隔
# plt.ylim(0,20)                                      #縦軸の範囲
# plt.xlim(-5,5)                                      #横軸の範囲
# plt.tick_params(axis="both",which="both",direction="in",
#         top=True,right=True,labelsize=40,width=1.7) #軸を内側にし文字の大きさ設定
# plt.ylabel("Electrostatic field (kV/cm)",size=50)   #縦軸のタイトル
# plt.xlabel("x (mm)",size=50)                        #横軸のタイトル
# plt.grid(which='major',color='gray')                #主軸を引く
# plt.legend()                                        #凡例を書く

# plt.savefig("/Users/ichige/Desktop/Ez_xprofile.pdf",bbox_inches="tight")
# plt.close()
# plt.show()

### z = 0 の電場強度分布 Ex ####
# plt.figure(figsize =(12,9))

# #電極の穴の直径 7.5 mm の強度分布
# plt.plot(np.arange(Ex75.shape[0])/10-20,(-Ex75[:,150]*1e-3),lw=5,color="r",label = "7.5 mm")
# #電極の穴の直径 15 mm の強度分布
# plt.plot(np.arange(Ex15.shape[0])/10-20,(-Ex15[:,150]*1e-3),lw=5,color="b",label = "15.0 mm")

# plt.yticks(np.arange(-20,21,5),np.arange(-20,21,5)) #縦軸のメモリ間隔
# plt.xticks(np.arange(-5,6,2.5),np.arange(-5,6,2.5)) #横軸のメモリ間隔
# plt.ylim(-10,10)                                    #縦軸の範囲
# plt.xlim(-5,5)                                      #横軸の範囲
# plt.tick_params(axis="both",which="both",direction="in",
#         top=True,right=True,labelsize=40,width=1.7) #軸を内側にし文字の大きさ設定
# plt.ylabel("Electrostatic field (kV/cm)",size=50)   #縦軸のタイトル
# plt.xlabel("x (mm)",size=50)                        #横軸のタイトル
# plt.grid(which='major',color='gray')                #主軸を引く
# plt.legend()                                        #凡例を書く
# #plt.savefig("/Users/ichige/Desktop/Ex_xprofile.pdf",bbox_inches="tight")
# plt.close()

# ### z = 0 の電場強度分布 Ez(15.0)/Ez(7.5) ####
# plt.figure(figsize =(12,9))

# # Ez(15.0)/Ez(7.5) の強度分布
# plt.plot(np.arange(Ez75.shape[0])/10-20,(Ez15[:,150])/(Ez75[:,150]),lw=5)

# plt.yticks(np.arange(0,3,0.5),np.arange(0,3,0.5))   #縦軸のメモリ間隔
# plt.xticks(np.arange(-5,6,2.5),np.arange(-5,6,2.5)) #横軸のメモリ間隔
# plt.ylim(0,2)                                       #縦軸の範囲
# plt.xlim(-5,5)                                      #横軸の範囲
# plt.tick_params(axis="both",which="both",direction="in",
#         top=True,right=True,labelsize=40,width=1.7) #軸を内側にし文字の大きさ設定
# plt.ylabel("Electrostatic field (kV/cm)",size=50)   #縦軸のタイトル
# plt.xlabel("x (mm)",size=50)                        #横軸のタイトル
# plt.grid(which='major',color='gray')                #主軸を引く
# #plt.savefig("/Users/ichige/Desktop/Ez_xprofile_ratio.pdf",bbox_inches="tight")
# #plt.close()

# ### x = 0 の電場強度分布 Ez ####
# plt.figure(figsize =(12,9))

# #電極の穴の直径 7.5 mm の強度分布
# plt.plot(np.arange(Ez75.shape[1])/10,(Ez75[200,:]*1e-3),lw=5,color="r",label = "7.5 mm")
# #電極の穴の直径 15 mm の強度分布
# plt.plot(np.arange(Ez15.shape[1])/10,(Ez15[200,:]*1e-3),lw=5,color="b",label = "15.0 mm")

# plt.yticks(np.arange(0,21,5),np.arange(0,21,5))      #縦軸のメモリ間隔
# plt.xticks(np.arange(10,21,2.5),np.arange(-5,6,2.5)) #横軸のメモリ間隔
# plt.ylim(0,20)                                       #縦軸の範囲
# plt.xlim(10,20)                                      #横軸の範囲
# plt.tick_params(axis="both",which="both",direction="in",
#         top=True,right=True,labelsize=40,width=1.7) #軸を内側にし文字の大きさ設定
# plt.ylabel("Electrostatic field (kV/cm)",size=50)   #縦軸のタイトル
# plt.xlabel("z (mm)",size=50)                        #横軸のタイトル
# plt.grid(which='major',color='gray')                #主軸を引く
# plt.legend(loc = "upper right")                     #凡例を書く

# #plt.savefig("/Users/ichige/Desktop/Ez_zprofile.pdf",bbox_inches="tight")
# #plt.close()

# ### x = 0 の電場強度分布 Ex ####
# plt.figure(figsize =(12,9))

# #電極の穴の直径 7.5 mm の強度分布
# plt.plot(np.arange(Ex75.shape[1])/10,(-Ex75[200,:]*1e-3),lw=5,color="r",label = "7.5 mm")
# #電極の穴の直径 15 mm の強度分布
# plt.plot(np.arange(Ex15.shape[1])/10,(-Ex15[200,:]*1e-3),lw=5,color="b",label = "15.0 mm")

# plt.yticks(np.arange(-20,21,5),np.arange(-20,21,5))  #縦軸のメモリ間隔
# plt.xticks(np.arange(10,21,2.5),np.arange(-5,6,2.5)) #横軸のメモリ間隔
# plt.ylim(-10,10)                                     #縦軸の範囲
# plt.xlim(10,20)                                      #横軸の範囲
# plt.tick_params(axis="both",which="both",direction="in",
#         top=True,right=True,labelsize=40,width=1.7) #軸を内側にし文字の大きさ設定
# plt.ylabel("Electrostatic field (kV/cm)",size=50)   #縦軸のタイトル
# plt.xlabel("z (mm)",size=50)                        #横軸のタイトル
# plt.grid(which='major',color='gray')                #主軸を引く
# plt.legend(loc = "upper right")                     #凡例を書く

# #plt.savefig("/Users/ichige/Desktop/Ex_zprofile.pdf",bbox_inches="tight")
# #plt.close()


# ### x = 0 の電場強度分布 Ez(15.0)/Ez(7.5) ####
# plt.figure(figsize =(12,9))

# # Ez(15.0)/Ez(7.5) の強度分布
# plt.plot(np.arange(Ez75.shape[1])/10,(Ez15[200,:])/(Ez75[200,:]),lw=5)

# plt.yticks(np.arange(0,3,0.5),np.arange(0,3,0.5))    #縦軸のメモリ間隔
# plt.xticks(np.arange(10,21,2.5),np.arange(-5,6,2.5)) #横軸のメモリ間隔
# plt.ylim(0,2)                                        #縦軸の範囲
# plt.xlim(10,20)                                      #横軸の範囲
# plt.tick_params(axis="both",which="both",direction="in",
#         top=True,right=True,labelsize=40,width=1.7) #軸を内側にし文字の大きさ設定
# plt.ylabel("Electrostatic field (kV/cm)",size=50)   #縦軸のタイトル
# plt.xlabel("x (mm)",size=50)                        #横軸のタイトル
# plt.grid(which='major',color='gray')                #主軸を引く
# #plt.savefig("/Users/ichige/Desktop/Ez_zprofile_ratio.pdf",bbox_inches="tight")
# #plt.close()

# plt.show()


# # Ez の場合
# plt.figure(figsize =(12,9))
# #z=0,0.5,1,-0.5,-1
# label = ["0 mm","0.5 mm","1 mm"]
# print(Ez75.shape)
# #電極の穴の直径 13 mm の強度分布
# for i in range(3):
#     print(i*50+200)
#     plt.plot(np.arange(Ez75.shape[1])/10,(Ez15[i*50+200,:]*1e-3),lw=5,label = label[i])

# plt.yticks(np.arange(0,21,5),np.arange(0,21,5))      #縦軸のメモリ間隔
# plt.xticks(np.arange(10,21,2.5),np.arange(-5,6,2.5)) #横軸のメモリ間隔
# plt.ylim(0,20)                                       #縦軸の範囲
# plt.xlim(10,20)                                      #横軸の範囲
# plt.tick_params(axis="both",which="both",direction="in",
#         top=True,right=True,labelsize=40,width=1.7) #軸を内側にし文字の大きさ設定
# plt.ylabel("Electrostatic field (kV/cm)",size=50)   #縦軸のタイトル
# plt.xlabel("z (mm)",size=50)                        #横軸のタイトル
# plt.grid(which='major',color='gray')                #主軸を引く
# plt.legend(loc = "upper right")                     #凡例を書く

# plt.savefig("/Users/ichige/Desktop/Ez_zprofile.pdf",bbox_inches="tight")
# #plt.close()
# #plt.show()

# # Ex の場合
# plt.figure(figsize =(12,9))
# #z=0,0.5,1,-0.5,-1
# E = ["Ez","Ex"]
# label = ["0 mm","0.5 mm","1 mm"]
# print(Ez75.shape)
# #電極の穴の直径 13 mm の強度分布
# for i in range(3):
#     print(i*50+200)
#     plt.plot(np.arange(Ex75.shape[1])/10,(Ex15[i*50+200,:]*1e-3),lw=5,label = label[i])

#     plt.yticks(np.arange(-20,21,5),np.arange(-20,21,5))      #縦軸のメモリ間隔
#     plt.xticks(np.arange(10,21,2.5),np.arange(-5,6,2.5)) #横軸のメモリ間隔
#     plt.ylim(-10,10)                                       #縦軸の範囲
#     plt.xlim(10,20)                                      #横軸の範囲
#     plt.tick_params(axis="both",which="both",direction="in",
#                     top=True,right=True,labelsize=40,width=1.7) #軸を内側にし文字の大きさ設定
#     plt.ylabel("Electrostatic field (kV/cm)",size=50)   #縦軸のタイトル
#     plt.xlabel("z (mm)",size=50)                        #横軸のタイトル
#     plt.grid(which='major',color='gray')                #主軸を引く
#     plt.legend(loc = "upper right")                     #凡例を書く

# plt.savefig("/Users/ichige/Desktop/%s_zprofile.pdf"%(E[1]),bbox_inches="tight")
# #plt.close()
# plt.show()

# E_sample = np.loadtxt("/Users/ichige/Desktop/normal/10kV_7.5mm/phi.txt")
# f,ax = plt.subplots(1,figsize=(12,9))
# ax.imshow(E_sample)
# print(E_sample[349,225])
Ez_test_l300d300 = np.loadtxt(
    "./data/Ez.txt", delimiter=",")
phi_test_l300d300 = np.loadtxt(
    "./data/phi.txt", delimiter=",")
Ey_test_l300d300 = np.loadtxt(
    "./data/Ex.txt", delimiter=",")

Ez_test_l600d300 = np.loadtxt(
    "./data/Ez.txt", delimiter=",")
phi_test_l600d300 = np.loadtxt(
    "./data/phi.txt", delimiter=",")
Ey_test_l600d300 = np.loadtxt(
    "./data/Ex.txt", delimiter=",")

Ez_d50 = np.loadtxt(
    "./data/Ez.txt", delimiter=",")
Ex_d50 = np.loadtxt(
    "./data/Ex.txt", delimiter=",")
phi_d50 = np.loadtxt(
    "./data/phi.txt", delimiter=",")


Ez_d50_bias = np.loadtxt(
    "./data/Ez.txt", delimiter=",")
Ex_d50_bias = np.loadtxt(
    "./data/Ex.txt", delimiter=",")
phi_d50_bias = np.loadtxt(
    "./data/phi.txt", delimiter=",")

Ez_5013 = np.loadtxt(
    "./data/Ez.txt", delimiter=",")
Ex_5013 = np.loadtxt(
    "./data/Ex.txt", delimiter=",")
phi_5013 = np.loadtxt(
    "./data/phi.txt", delimiter=",")

Ez_5013_bias = np.loadtxt(
    "./data/Ez.txt", delimiter=",")
Ex_5013_bias = np.loadtxt(
    "./data/Ex.txt", delimiter=",")
phi_5013_bias = np.loadtxt(
    "./data/phi.txt", delimiter=",")

Ez = np.loadtxt(
    "./data/Ez.txt", delimiter=",")
Ex = np.loadtxt(
    "./data/Ex.txt", delimiter=",")
phi = np.loadtxt(
    "./data/phi.txt", delimiter=",")

Ez_bias = np.loadtxt(
    "./data/Ez.txt", delimiter=",")
Ex_bias = np.loadtxt(
    "./data/Ex.txt", delimiter=",")
phi_bias = np.loadtxt(
    "./data/phi.txt", delimiter=",")


# ゼミ #
f, ax = plt.subplots(1, figsize=(12, 9))
im = plt.imshow(Ez/100, cmap="seismic")
plt.yticks(np.arange(0, 401, 50), np.arange(-20, 21, 5))  # 縦軸のメモリ間隔 d=100
plt.xticks(np.arange(0, 301, 50), np.arange(-15, 16, 5))  # 横軸のメモリ間隔 d=100
# plt.yticks(np.arange(0,401,50), np.arange(-20,21,5)) #d=50
# plt.xticks(np.arange(0,251,50),np.arange(-12.5,12.6,5))  #d=50
ax.tick_params(axis="both", width=1.5, size=20, labelsize=40, direction="in", top=True, right=True)  # 主目盛り．
# ax.set_ylim(49,351) #横軸の範囲指定
# ax.set_xlim(50,251) #縦軸の範囲指定
# ax.set_xlabel("z (pixel)",size=50) #縦軸のタイトル
# ax.set_ylabel("x (pixel)",size=50) #横軸のタイトル
ax.set_xlabel("z (mm)", size=50)  # 縦軸のタイトル
ax.set_ylabel("x (mm)", size=50)  # 横軸のタイトル

# color bar #
ax = plt.gca()
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(im, cax=cax)
plt.tick_params(axis="y", labelsize=40, direction="in",
                top="True", right="True", size=10)
plt.tick_params(axis="y", which="minor", size=5)
plt.clim(-15, 15)
cbar.set_label(label="Potential (kV)", size=40)
cbar.set_label(label="Electrostatic field $E_\mathrm{z}$(KV/cm)", size=40)
plt.tight_layout()
plt.savefig("./data/Ez_l75t75d100.pdf",
            bbox_inches="tight")
# plt.close()
# plt.show()

# 電場 Ex #
# rironn = np.ones(Ez_test_d200.shape[0])
x = np.arange(51, 151, 1)
x = np.arange(51, 451, 1)
# print(x)
# print(rironn.shape)
fig, ax = plt.subplots(1, figsize=(12, 9))
# ax.plot(-phi_test_max[200,:]/1000,color = "r",linewidth=5,label = "result")
# ax.plot(phi_test_l300d300[200,:]/1000,color = "r",linewidth=5,label = "result")
ax.plot(-Ez[200, :]/100, color="r", linewidth=5)
ax.plot(Ez_bias[200, :]/100, color="b", linewidth=5)
# print(Ex_test_remake[150,100],Ey_test[150,100])
# ax.plot(-phi_test_math_a[200,:]/1000,color = "b",linewidth=5)
# ax.plot(rironn*10,label = "theory")
# ax.plot(x,-15+0.1*(x-100),label = "theory")

# ax.plot(rironn*10,color = "b",linewidth=5)
# ax.plot(-Ey_d50[200,:]/100,color = "b",linewidth=5)
plt.xticks(np.arange(0, 301, 25), np.arange(-15, 15.1, 2.5))  # 横軸のメモリ間隔
# plt.xticks(np.arange(0,251,25),np.arange(-12.5,12.6,2.5))  #d=50
ax.set_ylim(0, 15)  # 縦軸の範囲指定
# ax.set_ylim(-10.10)
ax.set_xlim(100, 200)  # 横軸の範囲指定
# ax.set_xlim(100,150) #横軸の範囲指定

ax.tick_params(axis="both", width=1.5, size=20, labelsize=40, direction="in", top=True, right=True)  # 主目盛り．
ax.minorticks_on()   # 補助目盛りを表示する．
ax.tick_params(axis="both", which="minor", width=1.0, size=10, labelsize=30, direction="in", top=True, right=True)  # 補助目盛り．
plt.ylabel("Electrostatic field $E_\mathrm{z}$(KV/cm)", size=50)  # 縦軸のタイトル
# plt.ylabel("Potential(KV)",size=50) #縦軸のタイトル

plt.xlabel("z (pixel)", size=50)  # 横軸のタイトル
plt.xlabel("z (mm)", size=50)  # 横軸のタイトル

ax.grid(which="both")
# ax.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0)
# ax.legend(loc="lower right")

plt.tight_layout()
plt.savefig("./data/Ez_l75t75d100_profile.pdf",
            bbox_inches="tight")
# print(np.mean(-Ex[200,100:200]/100),np.mean(-Ex_bias[200,100:200]/100)
# plt.close()
plt.show()
