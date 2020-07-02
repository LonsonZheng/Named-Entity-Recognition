import numpy as np
import matplotlib.pyplot as plt

def Read_list(filename):
    file = open(filename+".txt", "r")
    list_row = file.readlines()
    list_source = []
    for i in range(len(list_row)):
        column_list = list_row[i].strip().split("\t")  # 每一行split后是一个列表
        list_source.append(column_list)                # 在末尾追加到list_source
    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            list_source[i][j] = int(list_source[i][j])
    file.close()
    return list_source

def Sigmoid(x):
    S = 1 / (1+np.exp(-x))
    return S

x_train = Read_list("x_train")
x_prove = Read_list("x_prove")

global theta
theta = np.zeros([1500, 1], dtype=np.float)  # 初始theta
alpha = 0.0001
pre_list = []
rec_list = []
f1_list = []

def Batch(theta):  # 第i次梯度下降
    sum = np.zeros([1500, 1], dtype=np.float)
    for loc in range(1, len(x_train)):
        x_loc = np.zeros([1500, 1], dtype=np.float)
        x_loc[x_train[loc][0]-1][0] = 1
        x_loc[499+x_train[loc][1]][0] = 1
        x_loc[499+500+x_train[loc][2]][0] = 1
        g = Sigmoid(np.dot(theta.T, x_loc))
        sum += ((x_train[loc][3] - g)*x_loc)
        if loc % 2000 == 0 or loc == len(x_train):
            theta = theta + (alpha * sum)
            sum = np.zeros([1500, 1], dtype=np.float)
    return theta

print("迭代开始\n")
for epoch in range(1, 40):
    theta = Batch(theta)
    total_predictions = 0
    total_predictions_ac = 0
    total_nts = 0
    for loc in range(1, len(x_prove)):#for loc in range(800 * (epoch - 1) + 1, 800 * epoch):
        x_loc = np.zeros([1500, 1], dtype=np.float)
        x_loc[x_prove[loc][0] - 1][0] = 1
        x_loc[499 + x_prove[loc][1]][0] = 1
        x_loc[499 + 500 + x_prove[loc][2]][0] = 1
        if x_prove[loc][3] == 1:
            total_nts += 1
        if Sigmoid(np.dot(theta.T, x_loc)) > 0.5:
            total_predictions += 1
            if x_prove[loc][3] == 1:
                total_predictions_ac += 1
    precission = total_predictions_ac / total_predictions  # 查准率
    recall = total_predictions_ac / total_nts  # 查全率
    F1_measure = 2 * precission * recall / (precission + recall)  # F1-measure
    pre_list.append(precission)
    rec_list.append(recall)
    f1_list.append(F1_measure)
    print("*******************************************************************************")
    print("第{0}次迭代：\n实体总数：{1} 模型预测总数：{2} 正确预测数：{3} \nprecission:{4} recall:{5} F1-measure:{6}".format(epoch, total_nts, total_predictions, total_predictions_ac, precission, recall, F1_measure))
    # # print("theta:{}\n".format(theta))
x = range(1, 40)
y1 = pre_list
y2 = rec_list
y3 = f1_list
plt.plot(x, y1, color='blue', label='precision')
plt.plot(x, y2, color='green', label='recall')
plt.plot(x, y3, color='red', label='F1-measure')
plt.legend()
plt.xlabel('Number of Iterations')
plt.show()

# 测试
x_test = Read_list("x_test")
total_predictions = 0
total_predictions_ac = 0
total_nts = 0
for loc in range(1, len(x_test)):#for loc in range(800 * (epoch - 1) + 1, 800 * epoch):
    x_loc = np.zeros([1500, 1], dtype=np.float)
    x_loc[x_test[loc][0] - 1][0] = 1
    x_loc[499 + x_test[loc][1]][0] = 1
    x_loc[499 + 500 + x_test[loc][2]][0] = 1
    if x_test[loc][3] == 1:
        total_nts += 1
    if Sigmoid(np.dot(theta.T, x_loc)) > 0.5:
        total_predictions += 1
        if x_test[loc][3] == 1:
            total_predictions_ac += 1
precission = total_predictions_ac / total_predictions  # 查准率
recall = total_predictions_ac / total_nts  # 查全率
F1_measure = 2 * precission * recall / (precission + recall)  # F1-measure
print("测试结果：\n实体总数：{0} 模型预测总数：{1} 正确预测数：{2} \nprecission:{3} recall:{4} F1-measure:{5}".format(total_nts, total_predictions, total_predictions_ac, precission, recall, F1_measure))