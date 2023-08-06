'''

Author: Zeng Siwei
Date: 2020-12-17 11:10:15
LastEditors: Zeng Siwei
LastEditTime: 2021-07-12 20:29:44
Description: 

'''

import numpy as np
import pandas as pd

def find_topk_diverse(features, k = 100, threshold = 1e-9):
    list_div = []
    selected_set = set()
    for i in range(features.shape[0]):
        for j in range(features.shape[0]):
            if i >= j or i in selected_set or j in selected_set:
                continue
            d_cos = np.dot(features[i], features[j])
            if d_cos > threshold:
                continue
            d_mov = np.sum(np.abs(features[i] - features[j]))
            list_div.append((d_mov, i, j))
            selected_set.add(i)
            selected_set.add(j)
            
    list_sorted = sorted(list_div, key=lambda x:x[0], reverse=True)
    if len(list_sorted) >= k:
        return list_sorted[:k]
    else:
        return list_sorted




if __name__ == "__main__":
    feats = np.load("/Users/endlesslethe/PycharmProjects/easygraphs/input/cora_feature.npy", allow_pickle=True)
    print(feats.shape)
    print(feats[0][:30])
    # data = pd.DataFrame(feats)
    # print(data.shape)
    # print(data)
    # profile = pp.ProfileReport(data, minimal=True)
    # profile.to_file("your_report.html")

    list_div = find_topk_diverse(feats, 100)

    # print(list_div)
    # for score, u, v in list_div:
    #     print(score, u, v)
    #     print(feats[u][:30])
    #     print(feats[v][:30])

    with open("cora_pert.txt", "w") as f:
        for score, u, v in list_div:
            f.write("%s\t%s\t%s\n" % (u, v, score))