
'''
根据给定的labels.csv文件，对train里图像按类 化分出也给test测试集/ val
'''
import os
import pandas as pd
import random
import shutil
import math
from tqdm import tqdm



def mkPath(file):
    if not os.path.exists(file):
        os.makedirs(file)

def splitSet(train_path, labels_csv ,save_path, ratio):
    '''
    按照比例，安装每类中的比例ratio， 从train_path中复制相应的图片到 ../test/cls_0,  ../test/cls_1 ....
    '''
    cls_n = 25
    # 根据labels.csv 每个图片对应的类别，看每个类的样本总数
    data_frame = pd.read_csv(labels_csv, header=None,skiprows=1)
    # 将数据转换为二维列表
    data_list = data_frame.values.tolist()

    # 打印结果
    #print(data_list)
    # 第i行存放 类i的样本名称
    label_set = [[] for _ in range(cls_n)]
    # 记录每类样本数
    label_num = [0] * cls_n
    for item in data_list:
        label_set[int(item[1])].append(item[0])
        label_num[int(item[1])] += 1
    #print(label_set)
    print(label_num)
    print(sum(label_num))
    # 记录下每个类抽取的样本数量
    nots_lst = [0]*cls_n
    # 根据比例，从每个类中复制出对应数量的样本，保存到对应的目录下
    for i in tqdm(range(cls_n)):
        # 计算类 cls_i的测试样本数
        nots = math.ceil(label_num[i]*ratio)
        nots_lst[i] = nots
        # 从图片名列表中随机选择指定数量的图片
        selected_images = random.sample(label_set[i], nots)
        #创建test数据集中类 目录
        cls_path = os.path.join(save_path, str(i))
        #print(cls_path)
        # 在目标路径下，创建类名对应的文件夹
        mkPath(cls_path)
        # 从类的所有训练样本中 复制随机选择的图片到目标路径
        for img_name in selected_images:
            source_path = os.path.join(train_path, img_name)
            destination_path = os.path.join(cls_path, img_name)
            shutil.copyfile(source_path, destination_path)
    print("抽取完成")
    for nots in nots_lst:
        print(f'类-{i} 抽取的样本数：{nots}')






if __name__ == "__main__":
    splitSet(r"G:\PeasantIdentity\train", r"G:\PeasantIdentity\train.csv",r"G:\PeasantIdentity\yolov5_6.2\test",0.2)