'''

Author: Zeng Siwei
Date: 2020-11-30 15:22:04
LastEditors: Zeng Siwei
LastEditTime: 2020-11-30 15:22:04
Description: 

'''

def split_by_value(series, split_value):
    g1 = series <= split_value
    g2 = series > split_value
    print("Len of group1 (value <= %s) :%s" % (split_value, g1.sum()))
    print("Len of group2 (value > %s) :%s" % (split_value, g2.sum()))
    return g1, g2


def ttest_ind(data, g1, g2, equal_var, cols_delete = [], cols = []):
    '''

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
    '''
    if not cols:
        cols = data.columns
    cols = set(cols)
    for col_delete in cols_delete:
        cols.discard(col_delete) 

    dict_statistic = dict()
    dict_pvalue = dict()


    for col in cols:
        d1 = data[col][g1]
        d2 = data[col][g2]
        statistic, pvalue = stats.ttest_ind(d1, d2, equal_var=equal_var)
        dict_statistic[col] = statistic
        dict_pvalue[col] = pvalue
    return dict_statistic, dict_pvalue


def get_percent(data, group, cols_delete = [], cols = []):
    if not cols:
        cols = data.columns
    cols = set(cols)
    for col_delete in cols_delete:
        cols.discard(col_delete) 

    cnt = 0
    list_result = []
    max_min = -1
    min_max = 999999
    dict_min = dict()
    dict_max = dict()
    for col in cols:
        max_rank =  -1
        min_rank = 999999

        data_col = np.array(data[col])
        sorted_idx = np.argsort(data_col)

        n_data = len(data_col)
        n_group = len(group)
        
        for i, idx in enumerate(sorted_idx):
            if idx in group:
                max_rank = max(max_rank, i)
                min_rank = min(min_rank, i)
        
        dict_min[col] = 1.0 * min_rank / n_data
        dict_max[col] = 1.0 * max_rank / n_data

        cnt += 1
        if cnt % 10000 == 0:
            print("processed:", cnt)
    return dict_min, dict_max


def compute_p_value(filename, filename_dict, is_save = False):
    data_group = pd.read_csv("100.csv")
    print(data_group)
    g1, g2 = group_by(data_group, "急性高原病评分LLQ（分值越高，习服能力越差）", 3)

    data = pd.read_csv(filename)
    print(data.shape)

    _, dict_pvalue = ttest_ind(data, g1, g2, False, ["index", "LLQ"])
    # # cols = [str(x) for x in [655042, 644066, 614272, 589636, 559747, 523463, 521697, 502372, 488290, 452422]]
    # _, dict_pvalue = ttest_ind(data, g1, g2, False, ["index"], ["599368"])
    # print(dict_pvalue)
    
    gene_dict = load_dict(filename_dict)
    cnt = 0
    list_sig = []

    for key, value in dict_pvalue.items():
        if value < 0.05:
            list_sig.append((key, gene_dict[key], value))
            cnt += 1
    print("num of pvalue < 0.05:", cnt)
    list_sorted = sorted(list_sig, key = lambda x: x[1])
    print(list_sorted[:10])
    # print(dict_pvalue["208129"])

    if is_save:
        with open(filename.split(".")[0] + "_pvalue_dict.txt", "w") as wfp:
            for key, value in dict_pvalue.items():
                wfp.write("%s\t%s\t%s\n" % (key, gene_dict[key], value))

def get_percentail(filename_extract, filename_dict, gene = None):
    data = pd.read_csv("100.csv")
    print(data)
    g1, g2 = group_by(data, "急性高原病评分LLQ（分值越高，习服能力越差）", 6)

    data = pd.read_csv(filename_extract)
    print(data.shape)

    dict_min, dict_max = get_percent(data, g2, ["index", "LLQ"])
    list_min = [(u, v) for u, v in dict_min.items()]
    list_max = [(u, v) for u, v in dict_max.items()]

    col1 = sorted(list_min, key=lambda x:x[1])[-10:] # col_max_min
    col2 = sorted(list_max, key=lambda x:x[1])[:10] # col_min_max

    gene_dict = load_dict(filename_dict)    

    for i in range(10):
        print(col1[i][0], gene_dict[str(col1[i][0])], col1[i][1])

    for i in range(10):
        print(col2[i][0], gene_dict[str(col2[i][0])], col2[i][1])
        plot_gene_hist(col2[i][0], gene_dict)

def get_argmin_by_column(data, ignore_indices = [], ignore_col_names = []):
    '''

    Args: 
	
    Returns: 
	
    Usage: 
        filename = "100.csv"
        nl = TableLoader(filename, header = None, sep=',')
        print(nl.data)
        print(nl.data.iloc[1])

        dict_argmin = get_argmin_by_column(nl.data, [0, 11, 22])
        print(dict_argmin)
        set_sus = set(dict_argmin.values())
        print(set_sus)
    '''

    ignore_indices = set(ignore_indices)
    ignore_col_names = set(ignore_col_names)
    dict_argmin = dict()
    for i, col in enumerate(data.columns):
        if i in ignore_indices or col in ignore_col_names:
            continue
        argmin = np.argmin(np.array(data[col]))
        dict_argmin[col] = argmin
    return dict_argmin