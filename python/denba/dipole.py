# 基本 #
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import os
# multi core  #
import concurrent.futures


class Main():
    def __init__(self):  # 最初に読み込まれる関数
        # 初期設定 #
        self.save_path = "./data/"  # 保存先のディレクトリ
        # self.save_path = "C:/python/denba_charge/charge_dis_test_dis100/"
        # 計算領域 #
        self.z = np.arange(0, 201, 1)  # 電極の厚み方向 離したい距離＋110+1
        self.x = np.arange(0, 201, 1)  # 電極の長さ方向
        self.dz = 0.1  # 1 ピクセルあたりの実際の長さ． 1 pixel = 0.1mm
        self.dx = 0.1
        # 電極のパラメーター #
        self.voltage_charge = 0  # 電荷の印加電圧
        Cu = 8.94  # 銅密度　g/cm^3
        Cu_mol = 63.546  # 原子量　g/mol
        mol = 6.0*10e22  # 原子量/mol
        volume = np.pi*0.25  # 体積　cm^2
        e = 1.602*1e-19  # 電子の電荷 C
        self.rho_num = e*(Cu*1/Cu_mol*mol)/(1e-3**2)  # 電荷量 C/mm^2
        self.rho_num = 1e-8*(1e-3**2)  # C/mm^2
        self.e0 = 8.85*1e-12*1e3  # 真空の誘電率 F/m
        self.voltage_laser = 0  # レーザー入射側の印加電圧
        self.voltage_thz = -10*1e3  # thz 電磁波射出側の印加電圧
        self.diameter = 5  # 電荷の半径 0.5mm
        self.den_length = 300  # 電極の長さ (y 方向)
        self.den_thick = 50  # 電極の厚さ (x 方向)
        self.den_space = 100  # 電極対の間隔
        self.den_laser_diameter = 0  # レーザー入射側における電極の穴の直径
        self.den_thz_diameter = 0  # thz 電磁波射出側における電極の穴の直径
        self.den_move = 0  # 電極を伝搬軸からずらす量
        # 収束に用いるパラメーター #
        self.conv = 1e-5  # 近似に用いる定数．小さくするほど計算は正確になる．
        self.omega = 1.9  # 加速係数．近似計算を収束させる定数．1~2 の範囲で設定．d
        self.MaxErr = 100  # MaxErr の初期値．値が小さくなければ雑に設定してよい．
        
        # データーを入れる配列 #
        self.phi = np.zeros((self.z.shape[0], self.x.shape[0]))  # ポテンシャルを入れる空の配列
        self.rho = np.zeros((self.z.shape[0], self.x.shape[0]))  # ポテンシャルを入れる空の配列
        self.den = np.zeros((self.z.shape[0], self.x.shape[0]))  # 電極の位置を示す空の配列．den[i][j] ==1 が電極の位置
        self.Ez = np.zeros((self.z.shape[0], self.x.shape[0]))  # 電場 Ex を示す空の配列
        self.Ex = np.zeros((self.z.shape[0], self.x.shape[0]))  # 電場 Ey を示す空の配列
        # 電極の詳細な位置 #
        self.center = [int(len(self.z)/2), int(len(self.x)/2)]  # 計算領域の中央
        self.den_z = [self.den_space/2, self.den_space/2 + self.den_thick]  # 電極の厚みの範囲 [50,100]
        self.den_laser_x = [self.den_laser_diameter/2, self.den_length/2]  # レーザー入射側における電極の長さの範囲 [25,150]
        self.den_thz_x = [self.den_thz_diameter/2,  self.den_length/2]  # thz 電磁波射出側の電極の長さの範囲 [65,150]

        # 電荷の詳細な位置 #
        self.point_1 = (50, int(len(self.x)-1)/2)
        self.point_2 = (self.z[-1]-50, int(len(self.x)-1)/2)

    def Position(self):  # 電極にポテンシャルを代入
        print("電極に電位を与えます．")
        # 0 deg #
        # 計算領域でループ #
        # 中心の場合 #
        # for i in range(self.z.shape[0]): # x 方向
        #     for j in range(self.x.shape[0]): # y 方向
        #         if(((self.center[0]-self.z[i]))**2+((self.center[1]-self.x[j]))**2<=(self.diameter)**2):
        #             print(i,j)
        #             self.phi[i,j] = self.voltage_charge
        #             self.rho[i,j] = self.rho_num
        #             self.den[i,j] = 1

        # 電荷が 2 つの場合
        for i in range(self.z.shape[0]):  # x 方向
            for j in range(self.x.shape[0]):  # y 方向
                if (self.z[i] == self.point_1[0] and self.x[j] == self.point_1[1]):
                    self.rho[i, j] = - self.rho_num
                    self.den[i, j] = 1
                elif (self.z[i] == self.point_2[0] and self.x[j] == self.point_2[1]):
                    self.rho[i, j] = self.rho_num
                    self.den[i, j] = 1

                # if(((self.point_1[0]-self.z[i]))**2+((self.point_1[1]-self.x[j]))**2<=(self.diameter)**2):
                #     self.phi[i,j] = self.voltage_charge
                #     self.rho[i,j] = - self.rho_num
                #     self.den[i,j] = 1
                # elif(((self.point_2[0]-self.z[i]))**2+((self.point_2[1]-self.x[j]))**2<=(self.diameter)**2):
                #     self.rho[i,j] = self.rho_num
                #     self.den[i,j] = 1



        fig, ax = plt.subplots(1)
        plt.imshow(self.rho)
        # plt.plot(self.rho[:,200])
        # plt.xlim(50,60)
        # plt.ylim(50,60)
        plt.show()
    
    def Math_single(self):  # single coreでの計算．基本 multi core で計算する
        n = 0
        t1 = time.time()
        phi = Main.Position(self)
        while True:  # 収束するまでループ
            for i in range(self.z.shape[0]):
                for j in range(self.x.shape[0]):
                    if (self.z[0] < self.z[i] < self.z[-1]):
                        if (self.x[0] < self.x[j] < self.x[-1]):
                            if (self.den[i, j] == 0):
                                pre_phi = self.phi[i, j]
                                self.phi[i, j] = self.omega * 0.25 * (self.phi[i+1, j]+self.phi[i-1, j]+self.phi[i, j+1]+self.phi[i, j-1]) + pre_phi - self.omega*pre_phi  # 差分化ポアソン方程式の計算． 収束を早めるために加速係数 omega をかけている．収束したら omega = 1 にして再び計算する．
                                if (i == int(len(self.z) / 2 + 1) and j == int(len(self.x) / 2 + 1)):  # 計算領域の中央ならば
                                    CurErr = abs(1-abs(pre_phi/self.phi[i, j]))  # 収束の割合．これが限りなく 0 に近くまでループを回す．
            if (self.MaxErr > CurErr):  # 収束の割合が小さくなったら
                self.MaxErr = CurErr
            if (self.MaxErr < self.conv/10):  # 設定した収束の割合より，小さくなったら
                self.omega = 1  # 加速係数 omega を 1 にする．omega = 1 の時の差分化したポアソン方程式を計算する．
            if (self.MaxErr < self.conv/100):  # omega = 1 にしたあと，再び計算するため
                break
            n = n+1
            if (n % 100 == 0):
                print(n, self.phi[150, 200], CurErr, time.time()-t1)
                t1 = time.time()
                # break

    def Math_upper_left(self, phi):  # multi core での計算．左上の領域
        for i in self.z[1:self.center[0]]:  # 計算範囲．左半分
            for j in self.x[1:self.center[1]]:  # 計算範囲．上半分
                # if(self.den[i,j] == 0): # [i,j] の座標に電極が存在しないなら
                pre_phi = self.phi[i, j]  # 1 つ前の計算結果
                phi[i, j] = self.omega * 0.25 * (self.rho[i, j]*self.dz**2/self.e0+phi[i+1, j]+phi[i-1, j]+phi[i, j+1]+phi[i, j-1]) + pre_phi - self.omega*pre_phi  # 差分化ポアソン方程式の計算． 収束を早めるために加速係数 omega をかけている．収束したら omega = 1 にして再び計算する．
        return phi  # 計算結果を返す
    
    def Math_lower_left(self, phi):  # multi core での計算．左下の領域
        for i in self.z[self.center[0]:-1]:  # 計算領域．左半分
            for j in self.x[1:self.center[1]]:  # 計算領域．下半分
                # if(self.den[i,j] == 0):
                pre_phi = phi[i, j]
                phi[i, j] = self.omega * 0.25 * (self.rho[i, j]*self.dz**2/self.e0+phi[i+1, j]+phi[i-1, j]+phi[i, j+1]+phi[i, j-1]) + pre_phi - self.omega*pre_phi  # 差分化ポアソン方程式の計算． 収束を早めるために加速係数 omega をかけている．収束したら omega = 1 にして再び計算する．
        return phi

    def Math_upper_right(self, phi):  # multi core での計算．右上の領域
        for i in self.z[1:self.center[0]]:  # 計算領域．右半分
            for j in self.x[self.center[1]:-1]:  # 計算領域．上半分
                # if(self.den[i,j] == 0):
                pre_phi = phi[i, j]
                phi[i, j] = self.omega * 0.25 * (self.rho[i, j]*self.dz**2/self.e0+phi[i+1, j]+phi[i-1, j]+phi[i, j+1]+phi[i, j-1]) + pre_phi - self.omega*pre_phi  # 差分化ポアソン方程式の計算． 収束を早めるために加速係数 omega をかけている．収束したら omega = 1 にして再び計算する．
        return phi
    
    def Math_lower_right(self,phi): # multi core での計算．右下の領域
        for i in self.z[self.center[0]:-1]: # 計算領域．右半分
            for j in self.x[self.center[1]:-1]: # 計算領域．下半分
                #if(self.den[i,j] == 0):
                pre_phi = phi[i,j]
                phi[i,j] = self.omega * 0.25 * (self.rho[i,j]*self.dz**2/self.e0+phi[i+1,j]+phi[i-1,j]+phi[i,j+1]+phi[i,j-1]) + pre_phi - self.omega*pre_phi # 差分化ポアソン方程式の計算． 収束を早めるために加速係数 omega をかけている．収束したら omega = 1 にして再び計算する．
        return phi

    def Math_multi(self):  # multi core での計算．基本的にこちらを使う．
        n = 0  # 計算回数
        t1 = time.time()  # 計算時間
        phi = np.zeros((self.z.shape[0], self.x.shape[0]))  # ポテンシャル
        den_position = [int(self.center[0]-self.den_space/2+1), int(self.center[0]+self.den_space/2+1)]  # 電極間隔の左端と右端
        Main.Position(self)  # ポテンシャルを与える関数
        CurErr = np.zeros((self.z.shape[0], self.x.shape[0]))  # 一つ前の計算結果との差を入れる空の配列
        print("電位計算します．")
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:  # multi core を使用するための宣言．max_workers = 使用する cpu の数
            while True:
                phi = self.phi.copy()
                phi_ul = executor.submit(Main.Math_upper_left, self, phi)  # multi core で指定した関数を実行させる．左上の領域での計算
                phi_ll = executor.submit(Main.Math_lower_left, self, phi)
                phi_ur = executor.submit(Main.Math_upper_right, self, phi)
                phi_lr = executor.submit(Main.Math_lower_right, self, phi)
                phi_ul = phi_ul.result()  # 計算結果を受け取る．
                phi_ll = phi_ll.result()
                phi_ur = phi_ur.result()
                phi_lr = phi_lr.result()
                # .result により全ての領域での計算が終わるまで待機する．
                self.phi[0:self.center[0], 0:self.center[1]] = phi_ul[0:self.center[0], 0:self.center[1]]  # 左上の領域での計算結果を代入する
                self.phi[self.center[0]:, 0:self.center[1]] = phi_ll[self.center[0]:, 0:self.center[1]]
                self.phi[0:self.center[0], self.center[1]:] = phi_ur[0:self.center[0], self.center[1]:]
                self.phi[self.center[0]:, self.center[1]:] = phi_lr[self.center[0]:, self.center[1]:]
                # self.phi[1:-1,1:-1] = np.where(self.den[1:-1,1:-1] == 0,(phi[2:,1:-1]+phi[:-2,1:-1]+phi[1:-1,2:]+phi[1:-1,:-2])+(1-self.omega)*phi[1:-1,1:-1],self.voltage_laser)
                phi_max = np.max(abs(self.phi))  # 電極間での電位の最大値を代入
                CurErr = abs(self.phi-phi) / phi_max  # 1つ前の計算との誤差を代入．0で割らないために最大値を用いて誤差率を出している
                CurErr_max = np.max(CurErr) # 誤差率の最大値を取得
                if (CurErr_max < self.conv/10):  # 誤差率が指定した値の 1/10 になったら
                    self.omega = 1  # 加速係数を 1 にする．
                    print("omega=1")
                    # ここから普通のポアソン方程式で計算 ###
                if (CurErr_max < self.conv/100):  # 誤差率が指定した値の 1/100 になったら
                    break  # 計算終了
                n = n+1
                if (n % 100 == 0):  # 100 回計算するごとに途中経過を表示
                    print("n,phi[center],CurErr,time", n, self.phi[self.center[0], self.center[1]], CurErr_max, time.time()-t1)  # time.time()-t1 でt1 を宣言してからの時間を表示する
                    t1 = time.time()  # 計算時間を初期化
                    # break # デバック用
        print("計算終了")

    def Denba(self):  # 電場計算 V/mm
        print("電場計算します．")
        for i in range(self.z.shape[0]):  # x 方向
            for j in range(self.x.shape[0]):  # y 方向
                if (self.z[0] < self.z[i] < self.z[-1]):  # 計算領域の端を含めない
                    if (self.x[0] < self.x[j] < self.x[-1]):  # 計算領域の端を含めない
                        self.Ez[i, j] = ((self.phi[i-1, j]-self.phi[i+1, j])/(2*self.dz))  # 微分の定義から電場を求める．中央差分をとっている
                        self.Ex[i, j] = ((self.phi[i, j-1]-self.phi[i, j+1])/(2*self.dx))
        print("計算終了")

    def Make_txt(self):  # txt データの作成．
        print("txt データを作成します．")
        self.phi = self.phi.T
        self.Ez = self.Ez.T
        self.Ex = self.Ex.T
        print("配列の転置をしました．")

        os.makedirs(self.save_path, exist_ok=True)  # ディレクトリが存在しない場合，self.save_path のディレクトリを作成する．
        with open(self.save_path+"memo.txt", "w") as file:  # txt ファイルを作成し書き込む
            file.write("計算パラメーター\r\n")  # ()の中身を書き込み
            file.write("計算領域 z {} pixel, x {} pixel \r\n".format(len(self.z), len(self.x)))
            file.write("1 pixel あたりの長さ z {} mm, x {} mm \r\n".format(self.dz, self.dx))
            file.write("印加電場 レーザー入射側 {} v, 電磁波射出側 {} V\r\n".format(self.voltage_laser, self.voltage_thz))
            file.write("電極の長さ {} mm \r\n".format(self.den_length/10))
            file.write("電極の厚み {} mm \r\n".format(self.den_thick/10))
            file.write("電極の長さ {} mm \r\n".format(self.den_length/10))
            file.write("電極対の間隔 {} mm \r\n".format(self.den_space/10))
            file.write("レーザー入射側の穴径 {} mm \r\n".format(self.den_laser_diameter/10))
            file.write("電磁波射出側の穴径 {} mm \r\n".format(self.den_thz_diameter/10))
            file.write("電極とレーザー伝搬軸のズレ {} mm \r\n".format(self.den_move/10))

        np.savetxt(self.save_path+"phi.txt", self.phi, delimiter=",")
        np.savetxt(self.save_path+"Ez.txt", self.Ez, delimiter=",")
        np.savetxt(self.save_path+"Ex.txt", self.Ex, delimiter=",")
        print("txt データを作成しました．")
        print("txt データを作成しました．")


if __name__ == "__main__":  # この python ファイルを実行したら
    main = Main()  # Main クラスをインスタンス化
    # main.Position()
    main.Math_multi()  # multi core で計算
    main.Denba()  # 電場計算
    main.Make_txt()  # txt データの作成
    print("プログラム終了")
