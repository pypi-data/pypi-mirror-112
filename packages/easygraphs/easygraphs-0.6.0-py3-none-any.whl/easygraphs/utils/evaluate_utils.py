'''

Author: Zeng Siwei
Date: 2021-04-07 15:09:19
LastEditors: Zeng Siwei
LastEditTime: 2021-04-13 00:46:51
Description: 

'''

def PRmetrics(ids, x_score, x_count, args = None, short_name = None):
    import sys
    func_name = sys._getframe().f_back.f_code.co_name
    if not short_name:
        short_name = func_name

    from sklearn.metrics import roc_auc_score

    EPS = 1e-9
    n_label_one = len(ids)
    n_nodes = len(x_score)
    scores = 1.0 * x_score / (x_count+EPS)
    scores[x_count == 0] = np.average(scores) # for plotting
    
    # regard top samples as positive samples
    arg_score = np.argsort(-scores)

    logging.info(func_name + "() ARGS n_label_one " + str(n_label_one))
    logging.info(func_name + "() OUTPUT empty element %s in %s" %(str(np.sum(x_count == 0)) , n_nodes))
    logging.debug(func_name + "() OUTPUT x_cum_score " + str(x_score[:10]))
    logging.debug(func_name + "() OUTPUT x_count " + str(x_count[:10]))
    logging.debug(func_name + "() OUTPUT arg_score " + str(arg_score[:10]))
    logging.debug(func_name + "() OUTPUT sus_score " + str(scores[arg_score[:10]]))
    

    y_true = np.zeros(n_nodes)
    y_true[ids] = 1
    AUC = roc_auc_score(y_true, scores)
    
    logging.info(func_name + "() AUC: %s " % AUC)

    if args:
        plot_roc_curve(y_true, scores, args.dir_fig, short_name+"_%s"%args.global_step)
        for i in sorted(sus_recall_dict.keys()):
            args.writer.add_scalar("%s_%s" % (i, func_name), sus_recall_dict[i], args.global_step)
        args.writer.add_scalar("AUC_"+short_name, AUC, args.global_step)

        sus_scores = scores[ids]
        plot_distribution(scores, short_name + "_" + str(args.global_step), dir_output=args.dir_fig)
        plot_distribution(sus_scores, short_name + "_sus_" + str(args.global_step), dir_output=args.dir_fig, labels=ids)
    return sus_recall_dict, AUC

def precision_at_k(target_ids, id_rank, missing_ids=None, checkpoint = [10, 50, 100, 200, 500, 1000, 2000, 5000]):
    '''
    Args: 
	
    Returns: 
	
    Usage: 
        # regard top samples (score is higher) as positive samples (label == 1)
        id_rank = np.argsort(-scores)
    '''

    sus_recall_dict = dict()
    sus_node_set = set(list(ids))
    
    checkpoint = [x for x in checkpoint if x < n_label_one]
    checkpoint.append(n_label_one)

    n_tp = 0
    ptr = 0
    valid = 0
    check_ptr = 0

    while ptr < n_nodes:
        index = arg_score[ptr]
     
        ptr += 1
        if scores[index] >= 0:
            valid += 1
            if index in sus_node_set:
                n_tp += 1

            if check_ptr < len(checkpoint) and valid == checkpoint[check_ptr]:
                sus_recall_dict[valid] = n_tp
                logging.info(func_name + "() OUTPUT Precision@%s %s" % (valid, n_tp))
                check_ptr += 1

    logging.info(func_name + "() True positive: %s Total label one: %s" % (n_tp, n_label_one))

def plot_roc_curve(y_label, y_score, dir_fig, identifier = None):
    from sklearn.metrics import roc_curve
    import matplotlib.pyplot as plt
    #roc_curve输出为tpr、fpr假正和真正概率，且第二个参数一定要是概率估计或者置信度

    name = "roc_" + identifier
    fpr,tpr,thresholds = roc_curve(y_label, y_score, pos_label=1)

    #pos_labels设置的为感兴趣方的标签
    #predict_probs前面输出的是0的概率，后面输出的是1的概率，如果不清楚可以只用predict
    #查看结果与概率的对应情况
    #一般吧流失设置为1，续费设置为0，感兴趣的设置为1

    plt.plot(fpr,tpr,linewidth=2,label="ROC")
    plt.xlabel("false presitive rate")
    plt.ylabel("true presitive rate")
    plt.ylim(0,1.05)
    plt.xlim(0,1.05)

    plt.legend(loc=4)#图例的位置
    plt.savefig(dir_fig + name + ".png", dpi = 300)
    plt.close()