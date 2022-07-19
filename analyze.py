import pickle
from collections import defaultdict
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

# total users: 1082
# total articles: 4080
# my id: 157480
# my like rank: 125! (155)
# my comments rank: 192! (68.667)

def analyze(data, task):
    user_num_dic = defaultdict(int)
    ave_like_dic = defaultdict(int)
    ave_dis_dic = defaultdict(int)

    with open('./data/user_article_dic', 'rb') as user_article_data:
        user_article_dic = pickle.load(user_article_data)
        for user in user_article_dic:
            user_num_dic[user] = len(user_article_dic[user])
    with open('./data/user_likes_dic', 'rb') as like_data:
        like_dic = pickle.load(like_data)
    with open('./data/user_discussion_dic', 'rb') as dis_data:
        dis_dic = pickle.load(dis_data)
    with open('./data/user_name_dic', 'rb') as user_name_data:
        user_name_dic = pickle.load(user_name_data)

    for user in user_num_dic:
        ave_like_dic[user] = float(like_dic[user]/user_num_dic[user])
        ave_dis_dic[user] = float(dis_dic[user]/user_num_dic[user])

    total_like = sorted(like_dic.items(), key=lambda x: x[1], reverse=True)
    total_dis = sorted(dis_dic.items(), key=lambda x: x[1], reverse=True)
    ave_like_dic_order = sorted(ave_like_dic.items(), key=lambda x: x[1], reverse=True)
    ave_dis_dic_order = sorted(ave_dis_dic.items(), key=lambda x: x[1], reverse=True)

    if data == 'total likes':
        dic = total_like
    elif data == 'total comments':
        dic = total_dis
    elif data == 'average likes per article':
        dic = ave_like_dic_order
    elif data == 'average comments per article':
        dic = ave_dis_dic_order

    list = [['id', 'user name', 'score']]
    for k, v in dic:
        user_id = k
        user_name = user_name_dic[k]
        list.append([k, user_name, v])
    df = pd.DataFrame(list[1:],columns=list[0])

    if task == 'save_data':
        import csv
        df.to_csv('./data/{}.csv'.format(data))

    elif task == 'plot':
        plt.figure(figsize=(25, 16))
        sns.set_style("whitegrid")
        print('ploting...')
        ax = plt.subplot(111)
        plt.bar(df['id'], df['score'], width=0.5, lw=0)
        plt.xlim(0, user_name_dic.__len__())
        plt.xticks(rotation='vertical')
        ax.set_xlabel(..., fontsize=36)
        ax.set_ylabel(..., fontsize=36)
        # plt.scatter(125, 155, linewidths=10, edgecolors='r')
        plt.ylabel("{}".format(data))
        plt.xlabel("user id")
        plt.yticks(size=36)
        plt.xticks(size=8)
        plt.show()


def analyze_label():
    with open('./data/label_name_count_dic', 'rb') as label_name_count_data:
        label_name_count_dic = pickle.load(label_name_count_data)
    labels = sorted(label_name_count_dic.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(labels, columns=['label', 'times'])
    df.to_csv('./data/label_score.csv')

def generate_network():
    with open('./data/follow_list_dic', 'rb') as follow_list_data:
        follow_list_dic = pickle.load(follow_list_data)
    network = []
    for key in follow_list_dic:
        follow_list = follow_list_dic[key]
        for target in follow_list:
            network.append([int(key), int(target)])
    print(network.__len__())
    network = pd.DataFrame(network)
    network.to_csv('./data/network.csv')
    print('done')


if __name__ == "__main__":
    analyze('total likes', 'save_data')
    # analyze_label()
    # generate_network()