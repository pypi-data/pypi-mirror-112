'''

Author: Zeng Siwei
Date: 2020-11-30 15:31:46
LastEditors: Zeng Siwei
LastEditTime: 2020-11-30 15:31:46
Description: 

'''
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import roc_auc_score, classification_report
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC
# from sklearn.cluster import KMeans
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
# from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor

'''
Usage: 
	

    
'''



CLASSIFIERS = {"DT": ("sklearn.tree", "DecisionTreeClassifier"),
                "LR": ("sklearn.linear_model", "LogisticRegressionCV"),
                "RF": ("sklearn.ensemble", "RandomForestClassifier"),
                "SVM": ("sklearn.svm", "SVC"),
                "KMeans": ("sklearn.cluster", "KMeans"),
                "KNN": ("sklearn.neighbors", "KNeighborsClassifier"),
                "NB": ("sklearn.naive_bayes", "GaussianNB"),
                "GBDT": ("sklearn.ensemble", "GradientBoostingClassifier")
                }

CLASSIFIER_ARGS = {"GBDT":dict(
                        learning_rate=0.1,
                        n_estimators=10,
                        subsample=1,
                        min_samples_split=2,
                        min_samples_leaf=1,
                        max_depth=3,
                        init=None,
                        random_state=None,
                        max_features=None,
                        # alpha=0.9, 
                        verbose=0,
                        max_leaf_nodes=None,
                        warm_start=False
                        ),
                    "SVM":dict(
                        probability=True
                        ),
                    "KMeans": dict(
                        n_clusters = 2
                        ),
                    "LR": dict(
                        class_weight = "balanced", 
                        max_iter = 1000
                        )
                    }

def run_classifier(classifier, x_data, y_data):
    if classifier == "all":
        for classifier in CLASSIFIERS.keys():
            print()
            print("Classifier", classifier)
            run_classifier(classifier, x_data, y_data)
    else:
        mod_name, model_name = CLASSIFIERS[classifier]
        args = CLASSIFIER_ARGS.get(classifier, dict())
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, shuffle=True, stratify=y_data)
        # print(x_test)
        # print(y_test)
        
        model = train(mod_name, model_name, x_train, y_train, args)
        test(model, x_test, y_test)
    # output_prediction(y_pred, model_name)


def train(mod_name, model_name, x_train, y_train, args = dict()):
    import_mod = __import__(mod_name, fromlist = str(True))
    if hasattr(import_mod, model_name):
         f = getattr(import_mod, model_name)
    else:
        print("404")
        return []
    clf = f(**args)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_train)
    # acc = get_acc(y_pred, y_train)
    # print("Train Accuracy: %0.2f" % acc)
    print(classification_report(y_train, y_pred, zero_division=1))

    if hasattr(clf, "predict_proba"):
        y_pred_prob = clf.predict_proba(x_train)[:, 1]
        auc = roc_auc_score(y_train, y_pred_prob)
        print("Train AUC: %0.2f" % auc)
        print()
    
    # scores = cross_val_score(clf, x_train, y_train, cv=5)
    # print("CrossVal Train Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    return clf

def test(model, x_test, y_test):
    y_pred = model.predict(x_test)
    print(classification_report(y_test, y_pred, zero_division=1))
    # print(y_pred)
    # acc = get_acc(y_pred, y_test)
    # print("Test Accuracy: %0.2f" % acc)

    if hasattr(model, "predict_proba"):
        y_pred_prob = model.predict_proba(x_test)[:, 1]
        auc = roc_auc_score(y_test, y_pred_prob)
        print("Test AUC: %0.2f" % auc)

# def get_acc(y_pred, y_true):
#     right_num = (y_true == y_pred).sum()
#     return right_num/y_true.shape[0]

# def get_auc(y_pred, y_true):
#     return roc_auc_score(y_true, y_pred)

def output_prediction(y_pred, model_name):
    print(y_pred)
    data_predict = {"Id":range(1, n_samples_test+1), "Label":y_pred}
    data_predict = pd.DataFrame(data_predict)
    # data_predict.to_csv("dr output %s.csv" %model_name, index = False)
    print(data_predict)