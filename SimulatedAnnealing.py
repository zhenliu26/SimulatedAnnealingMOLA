from matplotlib import pyplot as plt
from osgeo import osr
from osgeo import gdal
import numpy as np
import time


def path_length(weight, path_list, Array1New, Array2New):  # 计算路径长度
    Array1True = (1 - (path_list - 1).astype(bool).astype(int)) * weight[0]
    Array2True = (1 - (path_list - 2).astype(bool).astype(int)) * weight[1]
    suit = np.sum(Array1True * Array1New) + np.sum(Array2True * Array2New)
    return suit


def new_path(path_list, size):
    # 二交换法
    change_head = np.random.randint(0, size)
    change_tail = np.random.randint(0, size)
    while(path_list[change_head]==path_list[change_tail]):
        change_head = np.random.randint(0, size)
        change_tail = np.random.randint(0, size)
    temp_path_list=path_list.copy()
    temp=temp_path_list[change_head]
    temp_path_list[change_head]=temp_path_list[change_tail]
    temp_path_list[change_tail]=temp

    return change_head, change_tail, temp_path_list

# difference between new method and old method
def diff_old_new(weight, path_list, new_path_list, Array1New, Array2New):  # 计算新旧路径的长度之差
    Array1True=(1 - (path_list - 1).astype(bool).astype(int))*weight[0]
    Array2True = (1 - (path_list - 2).astype(bool).astype(int)) * weight[1]
    past_suit = np.sum(Array1True*Array1New)+np.sum(Array2True*Array2New)
    Array1NewTrue = (1 - (new_path_list - 1).astype(bool).astype(int)) * weight[0]
    Array2NewTrue = (1 - (new_path_list - 2).astype(bool).astype(int)) * weight[1]
    new_suit = np.sum(Array1NewTrue * Array1New) + np.sum(Array2NewTrue * Array2New)
    delta_p = new_suit - past_suit
    return delta_p
# count time
start_time = time.time()

# read the rst file
MCEFinal = "../data/MCEFINAL.rst"
industrial = "../data/Industrial.rst"
Raster1 = gdal.Open(MCEFinal)
Array1 = Raster1.ReadAsArray()
Raster2 = gdal.Open(industrial)
Array2 = Raster2.ReadAsArray()

# MOLA = "../data/5000MOLA.rst"
# RasterM = gdal.Open(MCEFinal)
# ArrayM = Raster1.ReadAsArray()
# ArrayMNew=ArrayM.flatten()



print(Array1.shape)

Array1New=Array1.flatten()
Array2New=Array2.flatten()

# index
Weights=[0.5,0.5]
sizeSample=[5000,5000]

size=len(Array1New)
# print(np.sum(ArrayMNew))
# print(path_length(Weights, ArrayMNew, Array1New, Array2New))

T_start = 5000  # 起始温度
T_end = 1e-30  # 结束温度
a = 0.995  # 降温速率
Lk = 50  # 内循环次数,马尔科夫链长


path_list = np.zeros(size)# 初始化路径
path_list[:sizeSample[0]]=1
path_list[sizeSample[0]:(sizeSample[0]+sizeSample[1])]=2



# output
# output_filename = '../output/allocation.rst'
# XSize = Array1.shape[1]
# YSize = Array2.shape[0]
#
# GeoT = Raster1.GetGeoTransform()
# Projection = osr.SpatialReference()
# Projection.ImportFromWkt(Raster1.GetProjectionRef())
#
# # Write output
# driver = gdal.GetDriverByName('rst')
# dataset = driver.Create(output_filename, XSize, YSize, 1, gdal.GDT_Float32)
# dataset.SetGeoTransform(GeoT)
# dataset.SetProjection(Projection.ExportToWkt())
# dataset.GetRasterBand(1).WriteArray(Array1)

print('hello')
best_path = path_length(Weights, path_list, Array1New, Array2New)  # 初始化最好路径长度
print('初始路径:', path_list)
print('初始路径长度:', best_path)
best_path_temp = []  # 记录每个温度下最好路径长度
best_path_list = []  # 用于记录历史上最好路径
balanced_path_list = path_list  # 记录每个温度下的平衡路径
balenced_path_temp = []  # 记录每个温度下平衡路径(局部最优)的长度
while T_start > T_end:
    for i in range(Lk):
        # new_path_list=path_list
        head, tail, new_path_list = new_path(path_list, size)
        delta_p = diff_old_new(Weights, path_list, new_path_list, Array1New, Array2New)
        if delta_p > 0:  # 接受状态
            balanced_path_list = path_list = new_path_list
            new_len = path_length(Weights, path_list, Array1New, Array2New)
            if (new_len > best_path):
                best_path = new_len
                best_path_list = path_list
        elif np.random.random() < np.exp(delta_p / T_start):  # 以概率接受状态
            path_list = new_path_list
    path_list = balanced_path_list  # 继承该温度下的平衡状态（局部最优）
    T_start *= a  # 退火
    best_path_temp.append(best_path)
    balenced_path_temp.append(path_length(Weights, balanced_path_list, Array1New, Array2New))
    print(path_length(Weights, balanced_path_list, Array1New, Array2New))
    print(T_start)
print('结束温度的局部最优路径:', balanced_path_list)
print('结束温度的局部最优路径长度:', path_length(Weights, balanced_path_list, Array1New, Array2New))
print('最好路径:', best_path_list)
print('最好路径长度:', best_path)

np.savetxt("output.txt", best_path_list, newline=" ")

print("--- %s seconds ---" % (time.time() - start_time))
# show the result
# x = []
# y = []
# for point in best_path_list:
#     x.append(coordinate_dict[point][0])
#     y.append(coordinate_dict[point][1])
plt.figure(1)
plt.subplot(211)
plt.plot(balenced_path_temp)  # 每个温度下平衡路径长度
plt.subplot(212)
plt.plot(best_path_temp)  # 每个温度下最好路径长度
# plt.subplot(313)
# plt.scatter(x, y)
# plt.plot(x, y)  # 路径图
# plt.grid()
plt.show()