import re
import numpy as np

def Save_list(list,filename):  # 保存列表到文本文件
    file = open(filename+".txt", "w")
    for i in range(len(list)):
        for j in range(len(list[i])):
            file.write(str(list[i][j]))
            file.write('\t')
        file.write('\n')
    file.close()

f = open("data_original.txt", "r", encoding='utf-8')  # 打开原始文件
fd = open("word_dic.txt", "r")  # 打开字典
fn = open("word_nt_dic.txt", "r")  # 打开nt字典
word_dic = eval(fd.read())
word_nt_dic = eval(fn.read())
lineage = 0  # 计行数
x_train = np.array([[0, 0, 0, 0]])  # 每个词的one-hot向量索引-训练集
x_prove = np.array([[0, 0, 0, 0]])  # 每个词的one-hot向量索引-验证集
x_test = np.array([[0, 0, 0, 0]])  # 每个词的one-hot向量索引-测试集

for line in f.readlines():  # 读取每行
    lineage += 1
    line = line[23:]  # 去除前23个字符
    words = line.split(' ')  # 行内按空格分割
    loc = np.array([[0, 0]])  # 当前词字典位置以及是否为nt
    for word in words:
        word_text = re.search(r'\W*([^\{]*)\{?.*\}?/([a-z]+)\W*', word)
        if word_text:
            if word_text.group(1) not in word_dic:
                if word_text.group(1) not in word_nt_dic:
                    loc = np.row_stack((loc, [[498, 0]]))
                else:
                    loc = np.row_stack((loc, [[498, 1]]))
            else:
                if word_text.group(1) not in word_nt_dic:
                    loc = np.row_stack((loc, [[word_dic[word_text.group(1)], 0]]))
                else:
                    loc = np.row_stack((loc, [[word_dic[word_text.group(1)], 1]]))
    if lineage < 14936:  # 训练集部分
        for i in range(1, loc.shape[0]):
            if i == 1:
                if i == len(loc) - 1:
                    x_train = np.row_stack((x_train, [[499, loc[i][0], 500, loc[i][1]]]))
                else:
                    x_train = np.row_stack((x_train, [[499, loc[i][0], loc[i+1][0], loc[i][1]]]))
            elif i == len(loc) - 1:
                x_train = np.row_stack((x_train, [[loc[i-1][0], loc[i][0], 500, loc[i][1]]]))
            else:
                x_train = np.row_stack((x_train, [[loc[i-1][0], loc[i][0], loc[i+1][0], loc[i][1]]]))
    elif lineage < 19967:  # 验证集部分
        for i in range(1, loc.shape[0]):
            if i == 1:
                if i == len(loc) - 1:
                    x_prove = np.row_stack((x_prove, [[499, loc[i][0], 500, loc[i][1]]]))
                else:
                    x_prove = np.row_stack((x_prove, [[499, loc[i][0], loc[i+1][0], loc[i][1]]]))
            elif i == len(loc) - 1:
                x_prove = np.row_stack((x_prove, [[loc[i-1][0], loc[i][0], 500, loc[i][1]]]))
            else:
                x_prove = np.row_stack((x_prove, [[loc[i-1][0], loc[i][0], loc[i+1][0], loc[i][1]]]))
    else:  # 测试集部分
        for i in range(1, loc.shape[0]):
            if i == 1:
                if i == len(loc) - 1:
                    x_test = np.row_stack((x_test, [[499, loc[i][0], 500, loc[i][1]]]))
                else:
                    x_test = np.row_stack((x_test, [[499, loc[i][0], loc[i+1][0], loc[i][1]]]))
            elif i == len(loc) - 1:
                x_test = np.row_stack((x_test, [[loc[i-1][0], loc[i][0], 500, loc[i][1]]]))
            else:
                x_test = np.row_stack((x_test, [[loc[i-1][0], loc[i][0], loc[i+1][0], loc[i][1]]]))
f.close()
fd.close()
fn.close()
Save_list(x_train, 'x_train')
Save_list(x_prove, 'x_prove')
Save_list(x_test, 'x_test')