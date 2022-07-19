import pickle
from collections import defaultdict
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt

# if True:
#     import powerlaw
#     with open('./data/user_likes_dic', 'rb') as like_data:
#         like_dic = pickle.load(like_data)
#     total_like = sorted(like_dic.items(), key=lambda x: x[1], reverse=True)
#     data = pd.DataFrame(total_like, columns=['id', 'num'])
#     data.index = data.index + 1
#     data = data.reset_index()
#     # sum = data['num'].sum()
#     # data['p'] = data['num'] / sum
#     data['log_num'] = np.log10(data['num'])
#     data['log_index'] = np.log10(data['index'])
#     y = data['num']
#     results = powerlaw.Fit(y)
#     a = (results.power_law.alpha)

if True:
    with open('./data/user_likes_dic', 'rb') as like_data:
        like_dic = pickle.load(like_data)
    total_like = sorted(like_dic.items(), key=lambda x: x[1], reverse=True)
    data = pd.DataFrame(total_like, columns=['id', 'num'])
    data.index = data.index + 1
    data = data.reset_index()
    # sum = data['num'].sum()
    data['p'] = data['num'] / sum
    data['log_num'] = np.log10(data['num'])
    data['log_index'] = np.log10(data['index'])
    print(data)
    plt.figure(figsize=(9, 9))
    ax = plt.subplot(111)
    ax.set_xlabel("user's rank", fontsize=18)
    ax.set_ylabel('number of likes', fontsize=18)
    sns.set_style("whitegrid")
    plt.xlim(-0.25, 3.2)
    plt.ylim(0,4.5)
    plt.axis([-0.25, 3.2, 0, 4.5])
    plt.xticks([0,1,2,3], ['10${^0}$', '10${^1}$','10${^2}$','10${^3}$'])
    plt.yticks([0,1,2,3,4], ['10${^0}$', '10${^1}$','10${^2}$','10${^3}$','10${^4}$'])
    plt.yticks(size=18)
    plt.xticks(size=18)
    plt.scatter(data['log_index'],data['log_num'])
    plt.show()

if False:
    with open('./data/user_discussion_dic', 'rb') as like_data:
        like_dic = pickle.load(like_data)
    total_like = sorted(like_dic.items(), key=lambda x: x[1], reverse=True)
    data = pd.DataFrame(total_like, columns=['id', 'num'])
    data.index = data.index + 1
    data = data.reset_index()

    sum = data['num'].sum()
    data['p'] = data['num'] / sum

    data['log_num'] = np.log10(data['num'])
    data['log_index'] = np.log10(data['index'])
    print(data)
    plt.figure(figsize=(9, 9))
    ax = plt.subplot(111)
    ax.set_xlabel("user's rank", fontsize=18)
    ax.set_ylabel('number of comments', fontsize=18)
    sns.set_style("whitegrid")
    plt.xlim(-0.25, 3.2)
    plt.ylim(0,4.5)
    plt.axis([-0.25, 3.2, 0, 4.5])
    plt.xticks([0,1,2,3], ['10${^0}$', '10${^1}$','10${^2}$','10${^3}$'])
    plt.yticks([0,1,2,3,4], ['10${^0}$', '10${^1}$','10${^2}$','10${^3}$','10${^4}$'])
    plt.yticks(size=18)
    plt.xticks(size=18)
    plt.scatter(data['log_index'],data['log_num'])
    plt.show()

if False:
    loss = [
        1.288,
        0.726,
        0.559,
        0.510,
        0.451,
        0.414,
        0.381,
        0.361,
        0.344,
        0.319,
        0.324,
        0.313,
        0.312,
        0.327,
        0.281,
        0.281,
        0.281,
        0.286,
        0.282,
        0.279,
        0.262,
        0.242,
        0.251,
        0.254,
        0.241,
        0.241,
        0.246,
        0.233,
        0.237,
        0.229,
        0.233,
        0.218,
        0.222,
        0.228,
        0.223,
        0.215,
        0.209,
        0.222,
        0.234,
        0.223,
        0.222,
        0.230,
        0.229,
        0.225,
        0.214,
        0.208,
        0.229,
        0.204,
        0.226,
        0.214,
        0.204,
        0.218,
        0.197,
        0.207,
        0.220,
        0.215,
        0.201,
        0.218,
        0.205,
        0.208,
        0.196,
        0.221,
        0.213,
        0.202,
        0.213,
        0.221,
        0.211,
        0.216,
        0.206,
        0.206,
        0.206,
        0.201,
        0.218,
        0.202,
        0.208,
        0.217,
        0.212,
        0.220,
        0.214,
        0.213,
        0.210,
        0.221,
        0.205,
        0.218,
        0.218,
        0.213,
        0.202,
        0.208,
        0.220,
        0.211,
        0.213,
        0.202,
        0.216,
        0.202,
        0.202,
        0.216,
        0.206,
        0.208,
        0.207,
        0.211,
        0.211,
        0.209,
        0.210,
        0.224,
        0.210,
        0.207,
        0.204,
        0.203,
        0.202,
        0.214,
        0.208,
        0.213,
        0.210,
        0.213,
        0.209,
        0.209,
        0.208,
        0.208,
        0.205,
        0.212,
        0.214,
        0.203,
        0.204,
        0.222,
        0.194,
        0.207,
        0.200,
        0.205,
        0.214,
        0.203,
        0.202,
        0.212,
        0.200,
        0.202,
        0.215,
        0.207,
        0.207,
        0.206,
        0.205,
        0.200,
        0.221,
        0.217,
        0.198,
        0.203,
        0.206,
        0.204,
        0.207,
        0.203,
        0.205,
        0.212,
        0.211,
        0.209,
        0.200,
        0.202,
        0.197,
        0.214,
        0.203,
        0.208,
        0.204,
        0.204,
        0.204,
        0.210,
        0.207,
        0.201,
        0.194,
        0.208,
        0.212,
        0.196,
        0.200,
        0.204,
        0.197,
        0.215,
        0.204,
        0.219,
        0.201,
        0.205,
        0.204,
        0.205,
        0.211,
        0.205,
        0.216,
        0.200,
        0.203,
        0.196,
        0.208,
        0.219,
        0.187,
        0.206,
        0.207,
        0.209,
        0.204,
        0.208,
        0.215,
        0.198,
        0.214,
        0.194,
        0.204,
        0.208,
        0.205,
        0.209,
        0.203,
        0.207,
        0.198,
        0.209,
        0.199,
        0.204,
        0.214,
        0.194,
        0.220,
        0.203,
        0.205,
        0.212,
        0.200,
        0.191,
        0.206,
        0.204,
        0.202,
        0.196,
        0.204,
        0.201,
        0.207,
        0.211,
        0.203,
        0.207,
        0.200,
        0.212,
        0.207,
        0.203,
        0.205,
        0.215,
        0.199,
        0.203,
        0.205,
        0.203,
        0.203,
        0.208,
        0.199,
        0.214,
        0.196,
        0.211,
        0.220,
        0.207,
        0.204,
        0.190,
        0.194,
        0.196,
        0.197,
        0.211,
        0.196,
        0.214,
        0.195,
        0.214,
        0.217,
        0.216,
        0.204,
        0.200,
        0.192,
        0.200,
        0.209,
        0.205,
        0.199,
        0.203,
        0.203,
        0.208,
        0.203,
        0.210,
        0.212,
        0.203,
        0.209,
        0.191,
        0.196,
        0.207,
        0.201,
        0.199,
        0.199,
        0.211,
        0.209,
        0.214,
        0.192,
        0.199,
        0.200,
        0.198,
        0.217,
        0.204,
        0.202,
        0.206,
        0.198,
        0.206,
        0.196,
        0.204,
        0.199,
        0.189,
        0.201,
        0.199,
        0.203,
        0.193,
        0.200,
        0.208,
        0.206,
        0.215,
        0.196,
        0.211,
        0.205,
        0.206,
        0.205,
        0.202,
        0.203,
        0.211
    ]
    plt.plot(loss)
    plt.xlabel("round")
    plt.ylabel("loss")
    plt.show()

# rmse: 0.2094, mae:0.1474
