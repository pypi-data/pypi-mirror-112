# 输入需要操作的库
# numpy是对矩阵进行操作
# math是对距离误差刻画时的平方开方进行操作
# pandas方便输出成excel数据
import numpy as np
import math
import pandas as pd

def Provenance(sample1, sample2, sample3):
    # p1，p2，p3表示各个abc源区的预测概率
    p1, p2, p3 = 0.0, 0.0, 1.0
    # 用于存放p1，p2，p3的列表
    add = []
    # 用于存放计算结果
    title = [['Partial of Provenance1', 'Partial of Provenance1', 'Partial of Provenance1', 'Variance']]
    # 创建空的dataframe
    last = pd.DataFrame(columns=title, dtype=float)

    # 矩阵求解思路如下：
    # （1）p1从0开始，以0.01的步长，逐步取值到1
    # （2）p2从1开始，以-0.01的步长，逐步取值到0
    # （3）p3等于1-p1-p2
    # （4）将取得值代入矩阵进行正向计算，与需要确定物源的岩石样品的岩石样品的Eu/Eu*，La/Yb，Gd/Yb值进行对比
    # （5）计算出的矩阵形式为（4，1），仅后三项与Eu/Eu*，La/Yb，Gd/Yb值逐一对应
    # （6）误差按照error=((Σ(xi-si)^2)^(1/2))/n,i=1,2,3,n=3 计算
    # 计数工具
    count = 0
    for p1 in range(0, 100, 1):
        for p2 in range(100, 0, -1):
            # 正向计算
            wait = np.array([[p1 / 100], [p2 / 100], [p3]])
            con = np.concatenate([sample1, sample2, sample3], 1)
            model = np.concatenate([wait.T, con])
            p3 = 1 - p1 / 100 - p2 / 100
            result = np.dot(model, wait)

            # 计算误差
            check = [result[1], result[2], result[3]]
            dev1 = ((float(check[0])) - (float(shale[0]))) ** 2
            dev2 = ((float(check[1])) - (float(shale[1]))) ** 2
            dev3 = ((float(check[2])) - (float(shale[2]))) ** 2
            dev = (math.sqrt(dev1 + dev2 + dev3)) / 3

            # 误差判定标准（误差计算标准是误差小于0.5，且各组分的含量不低于5%，
            # 这个标准是我初步试出来的，没有做定量的对比，还需要进一步对比）
            if dev < 0.4 and dev > 0 and p1 > 0.1 and p2 > 0.1 and p3 > 0.1:

                add = [[p1 / 100, p2 / 100, p3, dev]]
                count = count + 1
                # 用于存放中间变量
                add = pd.DataFrame(add, index=[count], columns=title, dtype=float)
                last = pd.concat([last, add], axis=0)

            else:
                continue
    return last

def Simulation(Sample1, Sample2, Sample3, Sample4):
    # 设置行和列的索引指标
    row = 0
    # 创建空的dataframe
    emulation = pd.DataFrame(dtype=float)
    for row in range(len(Sample1)):
        simu = (np.array(Sample1.iloc[row].iloc[0] * Sample2['平均值'] + Sample1.iloc[row].iloc[1] * Sample3['平均值'] +
                         Sample1.iloc[row].iloc[2] * Sample4['平均值']).reshape((14, 1)))
        simu = pd.DataFrame(simu.T, index=[row],
                            columns=['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
                                     'Lu'], dtype=float)
        emulation = pd.concat([emulation, simu], axis=0)
        row = row + 1
    return emulation

def Chondrite(sample):
    i = 0
    emulation = pd.DataFrame(dtype=float)
    chon = np.array(
        [[0.367], [0.957], [0.137], [0.711], [0.231], [0.087], [0.306], [0.058], [0.381], [0.0851], [0.249], [0.0356],
         [0.248], [0.0381]])
    for i in range(len(sample)):
        norm_chondrite = np.array(sample.iloc[i]) / chon.T
        norm_chondrite = pd.DataFrame(norm_chondrite, index=[i],
                            columns=['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
                                     'Lu'], dtype=float)
        norm_chon = pd.concat([emulation, norm_chondrite], axis=0)
        i = i + 1
    return norm_chon

# # 输入需要确定物源的岩石样品的Eu/Eu*，La/Yb，Gd/Yb值，所有数据均按照球粒陨石标准化
# shale = np.array([[0.71], [15.2], [1.95]])
#
# # 输入各个潜在物源样品Eu/Eu*，La/Yb，Gd/Yb值
# # 本次模拟中a代表HMBA，b代表dacites，c代表granitoids
# a = np.array([[0.9], [10.2], [1.91]])
# b = np.array([[0.83], [24.31], [3.13]])
# c = np.array([[0.64], [20.4], [2.07]])
#
# #计算潜在物源区比例
# Provenance_result = Provenance(a, b, c)
#
# #导入数据
# data_file_path = "C:\\Users\\Administrator\\Desktop\\待模拟数据.xlsx"
# # 导入各潜在物源的的微量元素，ppm
# a_aver = pd.read_excel(data_file_path, sheet_name='HMBA')
# b_aver = pd.read_excel(data_file_path, sheet_name='Dacites')
# c_aver = pd.read_excel(data_file_path, sheet_name='Granitoids')
#
# simu_result = Simulation(Provenance_result, a_aver, b_aver, c_aver)
# norm_simu = Chondrite(simu_result)
# print(norm_simu)