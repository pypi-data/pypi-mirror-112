'''

Author: Zeng Siwei
Date: 2020-10-16 10:40:38
LastEditors: Zeng Siwei
LastEditTime: 2021-04-02 00:37:22
Description: 

'''



def get_abspath(filepath):
    import inspect, os
    file = inspect.stack()[1][1]
    path = os.path.dirname(os.path.abspath(file))
    abspath = path + '/' + filepath
    return abspath


def load_function_by_reflection(full_function_name):
    tokens = full_function_name.split('.')
    module_name = ".".join(tokens[:-1])
    target = tokens[-1]

    module = __import__(module_name, fromlist=["xxx"])

    if hasattr(module, target):  # 判断在模块中是否存在对象
        target = getattr(module, target)  # 获取引用
        return target
    else:
        raise Exception("Load target function failed.")


def strip_postfix(filename):
    TEXT_FILE_POSTFIX = [".txt", ".csv", ".tsv", ".tensor", ".edgelist"]

    import re
    return re.sub("|".join(["("+x+")" for x in TEXT_FILE_POSTFIX]), "", filename)


def get_value_ratio_by_labels(x_object, labels):
    '''
    For a list of elements, using their labels to count the ratio at each value point.

    Returns: 
        dict_value_ratio

    Usage: 
        
    '''
    from collections import Counter, defaultdict
    import numpy as np
    
    x_object = np.array(x_object)
    dict_count = Counter(x_object) 
    dict_value_ratio = dict()
    n_labels = np.max(labels)+1
    n_values = len(dict_count)
    if n_values > 1000000:
        raise ValueError("Number of values must be less than 1000000.")

    x_ratio = np.zeros((n_labels, n_values))
    idmap = dict((x, i) for i, x in enumerate(dict_count.keys()))

    for i in range(n_labels):
        dict_class = Counter(x_object[labels==i]) 

        for value, count in dict_class.items():
            total = dict_count[value]
            ratio = count * 1.0 / total
            x_ratio[i][idmap[value]] = ratio
    x_ratio = x_ratio.T
    for key, id in idmap.items():
        dict_value_ratio[key] = list(x_ratio[id])
    return dict_value_ratio


def compute_fisher_p_value(size_intersection, size_result, size_target, size_background):
    """
    We use table
    |                | Aim Set      | Not Aim Set | Total |
    | ---            | ---                 | ---                | ---   |
    | Result Set     | size_intersection   |                    | size_result|
    | Non-result Set |                     |                    | size_background - size_result|
    | Total          | size_target         |                    | size_background |
    
    Args:
        size_result = len(set_result_id)
        size_background = 12298 = # affymetrix gene = len(set_backgroud)
        size_target = len(set_intersection_affymetrix_all)
    
    Returns:
        pvalue

    Note: 
        More details: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html

    """
    from scipy.stats import fisher_exact
    import logging
    logging.debug("Intersection Set Size:" + str(size_intersection) + "\tResult Set Size: " + str(size_result))
    logging.debug("Target Set Size:"+ str(size_target) + "\tBackground Set Size: " + str(size_background))
    oddsratio, pvalue = fisher_exact([[size_intersection, size_result-size_intersection],
                                        [size_target-size_intersection, size_background-size_target-size_result+size_intersection]])
    return pvalue

if __name__ == "__main__":
    print(compute_fisher_p_value(14, 100, 100, 2708))