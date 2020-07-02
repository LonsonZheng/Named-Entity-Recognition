import re

f = open("data_original.txt", "r", encoding='utf-8')#打开原始数据文件

word_dic_list = set()#记录所有的nt词
dic = {}#记录所有的词
word_dic = {}#生成字典
word_nt_dic = {}#生成nt字典
lineage = 0
for line in f.readlines():#读取每行
    lineage += 1
    line = line[23:]#去除前23个字符
    words = line.split(' ')#行内按空格分割
    for word in words:
        word_text = re.search(r'\W*([^\{]*)\{?.*\}?/([a-z]+)\W*', word)
        if word_text:
            if word_text.group(1) not in dic:
                if lineage < 14936:
                    dic[word_text.group(1)] = 1
                    if word_text.group(2) == 'nt':
                        word_dic_list.add(word_text.group(1))
            else:
                if lineage < 14936:
                    dic[word_text.group(1)] += 1
    words_com_nts = re.findall(r'\[([^\]]*)\]nt', line)#复合nt词
    for words_com_nt in words_com_nts:
        words_com_nt_split = words_com_nt.split(' ')
        for word_com_nt in words_com_nt_split:
            word_com_nt_text = re.search(r'\W*(.*)\{?.*\}?/([a-z]+)\W*', word_com_nt)
            if word_com_nt_text and word_com_nt_text.group(1) != '':
                word_dic_list.add(word_com_nt_text.group(1))
f.close()
word_nt_dic = dict(zip(word_dic_list, range(1, 5000)))
fn = open("word_nt_dic.txt", "w")
fn.write(str(word_nt_dic))
fn.close()  # nt文本字典
word_dic_list.clear()
all = sorted(dic.items(), key=lambda x: x[1], reverse=True)#排序
for item in all:
    if len(word_dic_list) < 497:
        if len(item[0]) != 0:
            word_dic_list.add(item[0])
        else:
            continue
    # elif len(word_dic_list) <497:
    #     if item[0] in word_nt_dic:
    #         word_dic_list.add(item[0])
    #     else:
    #         continue
    else:
        break
word_dic = dict(zip(word_dic_list, range(1, 500)))
ft = open("word_dic.txt", "w")
ft.write(str(word_dic))
ft.close()  # 文本字典