import urllib.request
from bs4 import BeautifulSoup
import re
import requests
import pickle
from collections import defaultdict
import time
import csv

# Regular Expression
find_article_id = re.compile(r'href="/articles/(.+?)" target="_blank">')
find_article_title = re.compile(r'target="_blank"><h3 class="am_card_title" title="(.+?)">')
find_article_category = re.compile(r'<a href="/categories/(.+?)"')
find_article_author_id = re.compile(r'href="/users/(.+?)" target="_blank">')
find_article_author_name = re.compile(r'<div class="avatar_text"><h3>(.+?)</h3>')
find_article_figure = re.compile(r'</path></svg>(.+?)</span>') # return ['15', '3'] or ['1.2k', '3.7k']
find_follow_page_num = re.compile(r'<a aria-label="Page (\d*?)"')
find_label_id = re.compile(r'<a class="label is_tags" href="/tags/(.+?)"')
find_label_name = re.compile(r'target="_blank">(.+?)</a>')
find_page_num = re.compile(r' <!-- -->(\d*?)<!-- --> ')

# history_u_lists, history_ur_lists:  user's interaction history, and his/her number of this interaction
# history_v_lists, history_vr_lists:  user set who have interacted with the label, and the times
history_u_lists = defaultdict(list)
history_ur_lists = defaultdict(list)
history_v_lists = defaultdict(list)
history_vr_lists = defaultdict(list)
label_lists = defaultdict(list)

def ask_url(url):
    head={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
    request = urllib.request.Request(url=url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except Exception as err:
        print(err)
    return html

def get_data(page_num_start, page_num_end):
    user_dic = defaultdict(list)
    user_name_dic = defaultdict(str)
    user_likes_dic = defaultdict(int)
    user_discussion_dic = defaultdict(int)
    for i in range(page_num_start, page_num_end):
        try:
            url = 'https://www.gcores.com/articles?page='+str(i)
            html = ask_url(url)
            soup = BeautifulSoup(html, 'html.parser')
            for item in soup.find_all("div", class_="am_card_inner"):
                item = str(item)
                user_id = (re.findall(find_article_author_id, item))[0]
                user_name = (re.findall(find_article_author_name, item))[0]
                article_id = (re.findall(find_article_id, item))[0]
                user_dic[user_id].append(article_id)
                user_name_dic[user_id] = user_name
                figure_list = re.findall(find_article_figure, item)
                if figure_list[0][-1] == 'k':
                    num_likes = int(float(figure_list[0][:-1]) * 1000)
                else:
                    num_likes = int(figure_list[0])
                if figure_list[1][-1] == 'k':
                    num_discussion = int(float(figure_list[1][:-1]) * 1000)
                else:
                    num_discussion = int(figure_list[1])
                user_likes_dic[user_id] += num_likes
                user_discussion_dic[user_id] += num_discussion
        except Exception as e:
            print(soup.find_all("div", class_="am_card_inner"))
            print(e)

        print(i)
        if i % 10 == 0:
            time.sleep(0.1)
            print('current page: {}: ({}%)'.format(i, round(((i - page_num_start) / (page_num_end - page_num_start))*100, 2)))

    print("saving...")
    save_pickle(user_name_dic, './data/user_name_dic')
    save_pickle(user_likes_dic, './data/user_likes_dic')
    save_pickle(user_discussion_dic, './data/user_discussion_dic')
    return

def get_follow(id):
    follow_list = []
    try:
        user_url = 'https://www.gcores.com/users/{}/follow?tab=followees'.format(id)
        html = ask_url(user_url)
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all("div", class_="profilePage"):
            item = str(item)
            page_num_data = re.findall(find_follow_page_num, item)
            page_num = 1 if page_num_data == [] else page_num_data[-1]
        head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
        url = 'https://www.gcores.com/gapi/v1/users/{}/followees?page[limit]=12&page[offset]=0'.format(id)
        for page in range(int(page_num)):
            params = {'page[limit]': 12, 'page[offset]': page*12}
            result = requests.get(url, headers=head, params=params)
            result.encoding = result.raise_for_status()
            html = result.json()
            data = html['data']
            for follow in data:
                follow_list.append(int(follow['id']))
                # print(follow['id'], follow['attributes']['nickname'])
                # print(follow['attributes']['followers-count']) # 被关注
                # print(follow['attributes']['followees-count']) # 已关注
                # print(follow['attributes']['location'])
    except Exception as err:
        print(err)
    return follow_list

def get_full_follow_list():
    follow_list_dic = defaultdict(list)
    with open('./data/user_name_dic', 'rb') as user_name_data:
        user_name_dic = pickle.load(user_name_data)
    i = 0
    for user_id in user_name_dic:
        i += 1
        if i % 10 == 0:
            print('current user: {} --- {}({}%)'.format(user_id, i, round(i/user_name_dic.__len__()*100,2)))
        follow_list = get_follow(user_id)
        follow_list_dic[user_id] = follow_list
    print("saving...")
    save_pickle(follow_list_dic, './data/follow_list_dic')


def get_article_list():
    with open('./data/user_article_dic', 'rb') as user_article_data:
        user_article_dic = pickle.load(user_article_data)
    total_article_list = []
    for author in user_article_dic:
        article_list = user_article_dic[author]
        total_article_list += article_list
    return total_article_list

def get_article():
    label_dic = defaultdict(str)
    label_id_count_dic = defaultdict(int)
    label_name_count_dic = defaultdict(int)

    label_users = defaultdict(list)

    total_article_list = get_article_list()

    num_ = 0
    for article in total_article_list:
        if num_ % 10 == 0:
            time.sleep(0.1)
            print('current article: {} --- ({}, {}%)'.format(article ,num_, round(num_/len(total_article_list)*100 , 2)))
        num_ += 1
        article_url = 'https://www.gcores.com/articles/{}'.format(article)
        html = ask_url(article_url)
        soup = BeautifulSoup(html, 'html.parser')
        labels = soup.find_all("div", class_="originalPage_labels")
        item = str(labels)
        label_id_list = re.findall(find_label_id, item)
        label_name_list = re.findall(find_label_name, item)

        # get label, label id, and label count
        for i, id in enumerate(label_id_list):
            label_name = label_name_list[i]
            label_dic[id] = label_name
            label_id_count_dic[id] += 1
            label_name_count_dic[label_name] += 1

        # get user's interaction
        comments_item = str(soup.find_all("p", class_="commentsMana_sortTabs"))
        comments_num = int(re.findall(find_page_num, comments_item)[0])
        comment_user_list = get_comments(article, comments_num)

        # generate label-users dic
        for id in label_id_list:
            label_users[id] += comment_user_list

    print("saving...")
    save_pickle(label_dic, "./data/label_dic")
    save_pickle(label_id_count_dic, "./data/label_id_count_dic")
    save_pickle(label_name_count_dic, "./data/label_name_count_dic")
    save_pickle(label_users, "./data/label_users")
    print("done")


def prepare_dataset():
    pass

def get_comments(article_id, comments_num):
    """
    Returns the id of users who have commented on an article.
    """

    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
    url =  'https://www.gcores.com/gapi/v1/articles/{}/comments?page[limit]=10&page[offset]=0&sort=-score&include=oldest-descendants,oldest-descendants.parent,oldest-descendants.user,user,subcommentable'.format(article_id)
    comments_page = (int(comments_num) // 10 + 1)
    user_list = []
    for page in range(int(comments_page)):
        params = {'page[limit]': 10, 'page[offset]': page*10}
        result = requests.get(url, headers=head, params=params)
        result.encoding = result.raise_for_status()
        html = result.json()
        if html['data'] == []:
            break
        data = html['included']
        for comment in data:
            if comment['type'] == 'users':
                user_list.append(comment['id'])
    return user_list

def get_social_adj_lists():
    social_adj_lists = defaultdict(lambda:{0})
    with open('./data/follow_list_dic', 'rb') as data:
        social_data = pickle.load(data)
    for user in social_data:
        if len(social_data[user]) != 0:
            social_adj_lists[int(user)] = set(social_data[user])
        else:
            social_adj_lists[int(user)] = set([0])
    save_pickle(social_adj_lists, './data/social_adj_lists')

def save_pickle(data, save_path):
    with open(save_path, 'wb') as save_file:
        pickle.dump(data, save_file)

if __name__ == '__main__':
    # get_article(['119673','119493','121351'])
    # get_comments('119673', 85)
    # get_article()
    get_social_adj_lists()
