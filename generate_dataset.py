import pickle
from collections import defaultdict

def generate_history_v():
    with open('./data/label_dic', 'rb') as f:
        label_dic = pickle.load(f)
    with open('./data/label_id_count_dic', 'rb') as f:
        label_id_count_dic = pickle.load(f)
    with open('./data/label_name_count_dic', 'rb') as f:
        label_name_count_dic = pickle.load(f)
    with open('./data/label_users', 'rb') as f:
        label_users = pickle.load(f)
    """
    ## toy dataset 
    history_u_lists, history_ur_lists:  user's purchased history (item set in training set), and his/her rating score (dict)
    history_v_lists, history_vr_lists:  user set (in training set) who have interacted with the item, and rating score (dict)
    
    train_u, train_v, train_r: training_set (user, item, rating)
    test_u, test_v, test_r: testing set (user, item, rating)
    
    social_adj_lists: user's connected neighborhoods
    ratings_list: rating value from 0.5 to 4.0 (8 opinion embeddings)
    """
    user_index_dic = {}
    label_index_dic = {}
    history_v_lists = defaultdict(list)
    history_vr_lists = defaultdict(list)
    for label in label_users:
        if label not in label_index_dic:
            label_index_dic[label] = int(label_index_dic.__len__())
        users_interaction_dic = defaultdict(int)
        users_interaction_list = label_users[label]
        # get the number of interaction for each user in this label
        for user_interaction in users_interaction_list:
                users_interaction_dic[user_interaction] += 1
        # for this label
        user_id_list = []
        user_interaction_list = []
        for user_id in users_interaction_dic:
            if user_id not in user_index_dic:
                user_index_dic[user_id] = int(user_index_dic.__len__())
            # key: user_id
            # value: interaction times
            user_id_list.append(int(user_index_dic[user_id]))
            times = int(users_interaction_dic[user_id])
            score = normalize(times)
            user_interaction_list.append(float(score))
        history_v_lists[int(label_index_dic[label])] = user_id_list
        history_vr_lists[int(label_index_dic[label])] = user_interaction_list

    print('saving...')
    save_pickle(user_index_dic, './data/user_index_dic')
    save_pickle(label_index_dic, './data/label_index_dic')
    save_pickle(history_v_lists, './data/history_v_lists')
    save_pickle(history_vr_lists, './data/history_vr_lists')

def generate_history_u():
    history_u_lists = defaultdict(list)
    history_ur_lists = defaultdict(list)
    with open('./data/history_v_lists', 'rb') as history_v_data:
        history_v_lists = pickle.load(history_v_data)
    with open('./data/history_vr_lists', 'rb') as history_vr_data:
        history_vr_lists = pickle.load(history_vr_data)

    train_index = 0
    for label in history_v_lists:
        for i, user in enumerate(history_v_lists[label]):
            score = float(history_vr_lists[label][i])
            history_u_lists[int(user)].append(int(label))
            history_ur_lists[int(user)].append(score)

    print('saving...')
    save_pickle(history_u_lists, './data/history_u_lists')
    save_pickle(history_ur_lists, './data/history_ur_lists')

def generate_social_adj_list():
    social_adj_lists = defaultdict(set)
    # 1082
    with open('./data/follow_list_dic', 'rb') as data:
        follow_list_dic = pickle.load(data)
    # 20633
    with open('./data/user_index_dic', 'rb') as data:
        user_index_dic = pickle.load(data)

    for user in follow_list_dic:
        if user not in user_index_dic:
            continue
        follow_list = []
        for followee in follow_list_dic[user]:
            if str(followee) not in user_index_dic:
                continue
            follow_list.append(int(user_index_dic[str(followee)]))
        if follow_list == []:
            follow_list = {0}
        social_adj_lists[int(user_index_dic[user])] = set(follow_list)
    save_pickle(social_adj_lists, './data/social_adj_lists')

def normalize(times):
    # {1.0: 0, 1.5: 1, 2.0: 2, 2.5: 3, 3.0: 4, 3.5: 5, 4.0: 6, 4.5: 7}
    if times == 1: # 1.5
        return 1.0
    elif times >= 2 and times < 4 : # 2.0
        return 2.0
    elif times >= 4 and times < 7 : # 2.5
        return 2.5
    elif times >= 7 and times < 15 : # 3.0
        return 3.0
    elif times >= 15 and times < 25: # 3.5
        return 3.5
    elif times >= 25 and times < 50: # 4.0
        return 4.0
    elif times >= 50 : # 4.5
        return 4.5

def save_pickle(data, save_path):
    with open(save_path, 'wb') as save_file:
        pickle.dump(data, save_file)

# 294
# 156
# 3.0 <- 2
if __name__ == '__main__':
    generate_history_v()
    generate_history_u()
    generate_social_adj_list()
