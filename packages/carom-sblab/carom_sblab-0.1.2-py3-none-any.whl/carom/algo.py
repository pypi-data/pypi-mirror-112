#!/usr/bin/env python
# coding: utf-8
"""
Created on Sat Oct 24 14:52:17 2020

@author: kirksmi
"""
from sklearn.metrics import confusion_matrix
import xgboost
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import (accuracy_score, f1_score, recall_score,
                             matthews_corrcoef, precision_score,
                             roc_curve, auc)
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
import warnings
import seaborn as sns
import copy
from sklearn.utils import class_weight
from sklearn.tree import DecisionTreeClassifier
from itertools import compress
from sklearn import tree
from sklearn.tree._tree import TREE_LEAF
# from dtreeviz.trees import *
# os.environ["PATH"] += os.pathsep + r"C:\\Users\\kirksmi\\anaconda3\\envs\\env\\lib\\site-packages\\graphviz"
# import graphviz
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import NearMiss
import math
from sklearn.model_selection import GridSearchCV
import shap
from collections import Counter
from matplotlib.lines import Line2D
import matplotlib.colors as mcol
import matplotlib.cm as pltcm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from matplotlib.ticker import FormatStrFormatter
import time
import sys
import matplotlib.cm as cm

shap.initjs()

# add library module to PYTHONPATH
sys.path.append(f"{os.getcwd()}/../")


def prune(tree):
    '''
    This function will get rid of repetitive branches in decision trees 
    which lead to the same class prediciton.
    Function written by GitHub user davidje13 (https://github.com/scikit-learn/scikit-learn/issues/10810)

    Function Inputs:
    ---------
    tree:   decision tree classifier

    Function Outputs:
    ---------
    tree:   pruned decision tree classifier
    '''
    tree = copy.deepcopy(tree)
    dat = tree.tree_
    nodes = range(0, dat.node_count)
    ls = dat.children_left
    rs = dat.children_right
    classes = [[list(e).index(max(e)) for e in v] for v in dat.value]
    leaves = [(ls[i] == rs[i]) for i in nodes]
    LEAF = -1
    for i in reversed(nodes):
        if leaves[i]:
            continue
        if leaves[ls[i]] and leaves[rs[i]] and classes[ls[i]] == classes[rs[i]]:
            ls[i] = rs[i] = LEAF
            leaves[i] = True
    return tree


def prune_index(inner_tree, index, threshold):
    '''
    This function will traverse a decision tree and remove any leaves with
    a count class less than the given threshold.
    Function written by David Dale
    (https://stackoverflow.com/questions/49428469/pruning-decision-trees)

    Function Inputs:
    ---------
    inner_tree:   tree object (.tree_) from decision tree classifier
    index:        where to start pruning tree from (0 for the root)
    threshold:    minimum class count in leaf 
    '''
    if inner_tree.value[index].min() < threshold:
        # turn node into a leaf by "unlinking" its children
        inner_tree.children_left[index] = TREE_LEAF
        inner_tree.children_right[index] = TREE_LEAF
    # if there are children, visit them as well
    if inner_tree.children_left[index] != TREE_LEAF:
        prune_index(inner_tree, inner_tree.children_left[index], threshold)
        prune_index(inner_tree, inner_tree.children_right[index], threshold)


def make_confusion_matrix(y_true=None,
                          y_pred=None,
                          cf=None,
                          group_names=None,
                          categories='auto',
                          count=True,
                          percent=True,
                          cbar=True,
                          xyticks=True,
                          xyplotlabels=True,
                          sum_stats=True,
                          figsize=(8, 6),
                          cmap='Blues',
                          title=None):
    '''
    This function will make a pretty plot of an sklearn Confusion Matrix
    using a Seaborn heatmap visualization.
    Basis of function from https://medium.com/@dtuk81/confusion-matrix-visualization-fc31e3f30fea

    Function Inputs:
    ---------
    y_true:        Array of experimental class labels
    y_pred:        Array of predicted class labels
    cf:            Can input pre-made confusion matrix rather than make one using y_true and y_pred.
    group_names:   List of strings that represent the labels row by row to be shown in each square.
    categories:    List of strings containing the categories to be displayed on the x,y axis. Default is 'auto'
    count:         If True, show the raw number in the confusion matrix. Default is True.
    cbar:          If True, show the color bar. The cbar values are based off the values in the confusion matrix.
                   Default is True.
    xyticks:       If True, show x and y ticks. Default is True.
    xyplotlabels:  If True, show 'True Label' and 'Predicted Label' on the figure. Default is True.
    sum_stats:     If True, display summary statistics below the figure. Default is True.
    figsize:       Tuple representing the figure size. Default will be the matplotlib rcParams value.
    cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is 'Blues'
                   See http://matplotlib.org/examples/color/colormaps_reference.html

    title:         Title for the heatmap. Default is None.
    '''

    # CODE TO GENERATE TEXT INSIDE EACH SQUARE

    if cf is None:
        cf = confusion_matrix(y_true, y_pred)

    blanks = ['' for i in range(cf.size)]
    hfont = {'fontname': 'Arial'}

    if group_names and len(group_names) == cf.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks

    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
    else:
        group_counts = blanks

    if percent:
        group_percentages = ["{0:.2%}".format(
            value) for value in cf.flatten()/np.sum(cf)]
    else:
        group_percentages = blanks

    box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(
        group_labels, group_counts, group_percentages)]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0], cf.shape[1])

    # CODE TO GENERATE SUMMARY STATISTICS & TEXT FOR SUMMARY STATS

    # if it is a binary or multi-class confusion matrix
    if len(categories) == 2:
        avg = "binary"
    else:
        avg = "macro"

    if y_true is None:
        diag = np.diagonal(cf)

        accuracy = sum(diag) / cf.sum()
        recalls = []
        precisions = []
        f1s = []
        mccs = []

        for i in range(len(categories)):
            nums = [*range(len(categories))]
            nums.remove(i)
            # print("Current nums: ", nums)
            TP = diag[i]
            FN = sum(cf[i, nums])
            TN = np.delete(np.delete(cf, i, 0), i, 1).sum()
            FP = sum(cf[nums, i])

            r = TP/(TP+FN)
            p = TP / (TP+FP)
            f = 2*(r*p)/(r+p)
            m = (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

            recalls.append(r)
            precisions.append(p)
            f1s.append(f)
            mccs.append(m)

        recall = np.mean(recalls)
        precision = np.mean(precisions)
        f1 = np.mean(f1s)
        mcc = np.mean(mccs)

    else:
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average=avg)
        recall = recall_score(y_true, y_pred, average=avg)
        f1 = f1_score(y_true, y_pred, average=avg)
        mcc = matthews_corrcoef(y_true, y_pred)
        # r = np.corrcoef(y_true, y_pred)[0, 1]

    if sum_stats:
        stats_text = "\n\nAccuracy={:0.3f}\nPrecision={:0.3f}\nRecall={:0.3f}\nF1 Score={:0.3f}\nMCC={:0.3f}".format(
            accuracy, precision, recall, f1, mcc)
    else:
        stats_text = ""

    if xyticks == False:
        # Do not show categories if xyticks is False
        categories = False

    if categories == 'auto':
        categories = range(len(categories))

    # MAKE THE HEATMAP VISUALIZATION
    fig, ax = plt.subplots(figsize=figsize)
    sns.set(font="Arial")
    ax = sns.heatmap(cf, annot=box_labels, fmt="",
                     cmap=cmap, cbar=cbar,
                     annot_kws={"size": 28})  # 22
    ax.set_yticklabels(labels=categories, rotation=90, va="center",
                       fontsize=24, **hfont)
    ax.set_xticklabels(labels=categories,
                       fontsize=24, **hfont)   # 20

    # FORMATTING THE CONFUSION MATRIX LABELS/TEXT
    # if labels, put stats to right of CM
    if xyplotlabels:
        plt.ylabel('True label', fontweight='bold', **hfont)
        plt.xlabel('Predicted label' + stats_text, fontweight='bold', **hfont)
    elif cbar:   # show color bar on right and stats below
        plt.xlabel(stats_text, fontsize=15, **hfont)
    else:   # no color or labels, so put stats on right
        ax.yaxis.set_label_position("right")
        ax.yaxis.set_label_coords(1.25, 0.75)
        plt.ylabel(stats_text, fontsize=18, rotation=0, **hfont)  # labelpad=75

    if title:
        plt.title(title, **hfont)

    plt.tight_layout()
    return ax


def train_model(X, y,  condition="CAROM", num_folds=5, class_names=None,
             depth="deep", imbalance="none", pos_label=1,
             random_seed=123, num_iter=25,
             fig_path='../figures/crossval/'):
    '''
    This function trains an XGBoost model for predicting post-translational
    modifications (the target array) given a features matrix.

    For binary models, the pos_label argument can be used to designate the 
    class of interest. 
    For multi-class models, it is assumed that the middle class is Unregulated
    and the lower/upper classes mark Phos and Acetyl, respectively
    (e.g -1=Phos, 0=Unreg, 1=Acetyl)

    The function uses RandomizedGridSearch within cross-validation to tune 
    the XGBoost hyperparameters and estimate model performance. The final model
    uses the hyperparameters from the best-scoring CV fold and is trained on 
    the entire dataset.


    Function Inputs:
    ---------
    1. X:            Predictor features matrix 
    2. y:            Target variable
    3. condition:    String used to identify dataset condition (e.g "e.coli").
                     Used to name/save plots.
    4. num_folds:    Number of cross-validation folds
    5. class_names:  Names of target classes   
    6. depth:        Determines the range of values for tuning the max_depth 
                     hyperparameter. Options are "deep" (default) or "shallow"
    7. imbalance     Determines the method for addressing class imbalance:
                     a.) List of two floats (for multi-class) or single float
                         (for binary): Model will use SMOTE oversampling for the
                         Phos/Acetyl classes. This assumes that Unregulated is
                         largest class. Ex: [0.5, 0.75] --> Phos class will be 
                         over-sampled to 50% of size of Unreg, Acetyl to 75% of
                         Unreg.
                     b.) "adasyn": uses Adasyn over-sampling method. Phos and                      
                         Acetyl classes over-sampled to 75% of Unreg class. 
                     c.) "undersample": undersamples larger classes to size of 
                         smallest class. 
                     d.) "none" (default): class balances are not adjusted
                     e.) "balanced": inverse proportion of classes are used to
                          assign class weights for "sample_weights" argument in 
                          hyperparameter tuning
    8. pos_label:    Used to identify class of interest for binary problems. Does
                     not affect multi-class problems.
    9. random_seed:  Random seed used for cross-validation splits and hyperparameter
                     tuning.
    10. num_iter:    Number of iterations to run for each fold of RandomizedGridSearch.
    11. fig_path:    Directory to save figures. Default is '../figures/crossval/'

    Function Outputs:
    ---------
    1. XGBoost model (fitted to entire dataset)
    2. Dataframe w/ XGBoost cross-val scores
    '''
    start = time.time()

    # define font type for plots
    pltFont = {'fontname': 'Arial'}

    # define feature names
    feat_names = X.columns

    # transform Target classes to 0, 1, 2 (this helps XGBoost)
    le = preprocessing.LabelEncoder()
    le.fit(y)
    y = pd.Series(le.transform(y))

    # if class names not given, use class integers
    if class_names is None:
        class_names = []
        for cl in y.unique():
            class_names.append(np.array2string(cl))

    num_class = len(np.unique(y))
    print("Number of class: {}".format(num_class))

    # hyperparameters to tune
    # (max_depth adjusted based on 'depth' argument)
    if depth == "shallow":
        params = {
            "learning_rate": [0.01, 0.05, 0.1, 0.3],
            "max_depth": range(3, 8, 1),  # range(4,11,2),
            "min_child_weight": [3, 5, 7, 10],
            "subsample": [0.7, 0.8, 0.9],
            "colsample_bytree": [0.7, 0.8, 0.9],
        }
    elif depth == "deep":
        params = {
            "learning_rate": [0.01, 0.05, 0.1, 0.3],
            "max_depth": range(4, 11, 2),
            "min_child_weight": [3, 5, 7],
            "subsample": [0.8, 0.9],
            "colsample_bytree": [0.8, 0.9]
        }

    ##### Cross-validation training #####

    # Define classifiers and hyperparameter search, based on binary vs multi-class problem
    if num_class == 2:
        print("TRAINING BINARY MODEL!")
        # define classifier and hyperparameter tuning
        classifier = xgboost.XGBClassifier(objective='binary:logistic',
                                           n_estimators=150,
                                           use_label_encoder=False,
                                           eval_metric='logloss',
                                           random_state=random_seed)

        random_search = RandomizedSearchCV(classifier, param_distributions=params,
                                           n_iter=num_iter, scoring='f1',
                                           n_jobs=-1, cv=num_folds, verbose=3,
                                           random_state=random_seed)
        avg = "binary"

    elif num_class > 2:
        print("TRAINING MULTI-CLASS MODEL!")
        classifier = xgboost.XGBClassifier(objective='multi:softmax',
                                           n_estimators=150,
                                           use_label_encoder=False,
                                           num_class=num_class,
                                           eval_metric='mlogloss',
                                           random_state=random_seed)  # multi:softmax

        random_search = RandomizedSearchCV(classifier, param_distributions=params,
                                           n_iter=num_iter, scoring='f1_macro',
                                           n_jobs=-1, cv=num_folds, verbose=3,
                                           random_state=random_seed)
        avg = "macro"

    # Stratified cross-val split
    cv = StratifiedKFold(n_splits=num_folds,
                         shuffle=True,
                         random_state=random_seed)

    # create empty lists to store CV scores, confusion mat, etc.
    acc_list = []
    recall_list = []
    precision_list = []
    f1_list = []
    mcc_list = []
    auc_list = []
    r_list = []

    y_test = []
    y_pred = []
    cmCV = np.zeros((num_class, num_class))

    paramDict = {}

    count = 0

    # loop through cross-val folds
    for train_index, test_index in cv.split(X, y):
        print("\n Cross-val Fold # {} \n".format(count))

        X_trainCV, X_testCV = X.iloc[train_index], X.iloc[test_index]
        y_trainCV, y_testCV = y.iloc[train_index], y.iloc[test_index]
        
        # train and fit model according to the desired class imbalance method
        if isinstance(imbalance, (list, float)):
            class_values = y_trainCV.value_counts()
            if num_class > 2:
                smote_dict = {0: int(round(class_values[1]*imbalance[0])),
                              1: class_values[1],
                              2: int(round(class_values[1]*imbalance[1]))}
            else:
                smote_dict = {0: class_values[0],
                              1: int(round(class_values[0]*imbalance))}

            print(smote_dict)
            oversample = SMOTE(sampling_strategy=smote_dict)
            X_trainCV, y_trainCV = oversample.fit_resample(
                X_trainCV, y_trainCV)
            random_search.fit(X_trainCV, y_trainCV)

        elif imbalance == "adasyn":
            class_values = y_trainCV.value_counts()
            smote_dict = {0: int(round(class_values[1]*0.75)),
                          1: class_values[1],
                          2: int(round(class_values[1]*0.75))}
            ada = ADASYN(sampling_strategy=smote_dict,
                         random_state=random_seed, n_neighbors=10)
            X_trainCV, y_trainCV = ada.fit_resample(X_trainCV, y_trainCV)
            random_search.fit(X_trainCV, y_trainCV)

        elif imbalance == "undersample":
            nr = NearMiss()
            X_trainCV, y_trainCV = nr.fit_sample(X_trainCV, y_trainCV)
            random_search.fit(X_trainCV, y_trainCV)

        elif imbalance == "none":
            random_search.fit(X_trainCV, y_trainCV)

        elif imbalance == "balanced":
            weights = class_weight.compute_sample_weight("balanced", y_trainCV)

            random_search.fit(X_trainCV, y_trainCV,
                              sample_weight=weights)

        # get best estimator from random search
        randomSearch_mdl = random_search.best_estimator_

        # tune gamma and get new best estimator
        params_gamma = {'gamma': [0, 0.1, 0.3, 0.5]}
        gamma_search = GridSearchCV(estimator=randomSearch_mdl,
                                    param_grid=params_gamma,
                                    scoring='f1_macro',
                                    n_jobs=-1, cv=3)
        gamma_search.fit(X_trainCV, y_trainCV)
        best_Mdl = gamma_search.best_estimator_

        # print and store best params for current fold
        print("Model Params: \n {}".format(best_Mdl))
        paramDict[count] = best_Mdl.get_params

        # make model predictions on X_testCV and store results
        y_predCV = best_Mdl.predict(X_testCV)
        y_proba = best_Mdl.predict_proba(X_testCV)

        y_test.extend(y_testCV)
        y_pred.extend(y_predCV)
        cm = confusion_matrix(y_testCV, y_predCV)
        print("current cm: \n", cm)
        cmCV = cmCV+cm   # update overal confusion mat
        print("Combined cm: \n", cmCV)

        # calculate auc
        if num_class > 2:
            mean_auc = plot_roc(best_Mdl,
                                X_trainCV, y_trainCV,
                                X_testCV, y_testCV,
                                class_names=class_names,
                                pos_class=pos_label,
                                figsize=(8, 6),
                                show=False)[0]
            # fig.savefig("../figures/crossval/{}_XGBcrossval_ROC{}.png".format(condition, count),
            #     dpi=600)
        else:
            preds = y_proba[:, pos_label]
            fpr, tpr, threshold = roc_curve(y_testCV, preds)
            mean_auc = auc(fpr, tpr)

        # calculate classification scores and store
        accuracy = accuracy_score(y_testCV, y_predCV)
        f1 = f1_score(y_testCV, y_predCV,
                      average=avg, pos_label=pos_label)
        recall = recall_score(y_testCV, y_predCV,
                              average=avg, pos_label=pos_label)
        precision = precision_score(y_testCV, y_predCV,
                                    average=avg, pos_label=pos_label)
        mcc = matthews_corrcoef(y_testCV, y_predCV)
        r = np.corrcoef(y_testCV, y_predCV)[0, 1]

        acc_list.append(accuracy)
        recall_list.append(recall)
        precision_list.append(precision)
        f1_list.append(f1)
        mcc_list.append(mcc)
        auc_list.append(mean_auc)
        r_list.append(r)

        count = count+1

    # print final confusion mat
    print("final CV confusion matrix: \n", cmCV)

    # plot confusion matrix results
    path = fig_path
    try:
        os.makedirs(path)
    except OSError:
        print("Directory already created")

    make_confusion_matrix(y_test, y_pred, figsize=(8, 6), categories=class_names,
                          xyplotlabels=True, cbar=False, sum_stats=False)
    plt.ylabel("Experimental Labels", fontsize=24)
    plt.xlabel("Predicted Labels", fontsize=24)
    plt.tight_layout()
    plt.savefig(path+"/{}_XGBcrossval_confusionMat.png".format(condition),
                dpi=600)
    plt.show()

    # get average scores
    Accuracy = np.mean(acc_list)
    F1 = np.mean(f1_list)
    Precision = np.mean(precision_list)
    Recall = np.mean(recall_list)
    MCC = np.mean(mcc_list)
    AUC = np.mean(auc_list)
    Corr = np.mean(r_list)

    scores = [Accuracy, Recall, Precision, F1, MCC, AUC, Corr]

    # get stats for CV scores
    loop_scores = {'Accuracy': acc_list,
                   'Recall': recall_list,
                   'Precision': precision_list,
                   'F1': f1_list,
                   'MCC': mcc_list,
                   'AUC': auc_list,
                   'R': r_list}

    df_loop_scores = pd.DataFrame(loop_scores)
    print("Model score statistics: ")
    loop_stats = df_loop_scores.describe()
    print(loop_stats)

    # plot CV scores
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['xtick.major.pad'] = '10'
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(df_loop_scores.columns, scores,
           yerr=loop_stats.loc['std', :],
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=10,
           width=0.8)
    ax.set_ylim([0, 1.0])
    plt.yticks(**pltFont)
    ax.set_xticks(df_loop_scores.columns)
    ax.set_xticklabels(df_loop_scores.columns, **pltFont,
                       rotation=45, ha="right", rotation_mode="anchor")
    ax.tick_params(axis='both', which='major', labelsize=24)
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.savefig(path+'/{}_XGB_crossVal_barGraph.png'.format(condition),
                bbox_inches='tight', dpi=600)
    plt.show()

    # create dataframe with mean scores
    data = {'Metric': ['Acc', 'Recall', 'Precision', 'F1', 'MCC', 'AUC', 'PearsonsR'],
            'Scores': [Accuracy, Recall, Precision, F1, MCC, AUC, Corr]}
    df_scores = pd.DataFrame(data)
    df_scores = df_scores.set_index('Metric')

    # train model on entire training dataset using params from best CV model
    maxpos = mcc_list.index(max(mcc_list))
    final_params = paramDict[maxpos]
    print("CV MCCs: {}".format(mcc_list))
    print("Best parameters: ", final_params)
    final_Mdl = classifier
    final_Mdl.get_params = final_params

    if isinstance(imbalance, (list, float)):
        class_values = y.value_counts()
        if num_class > 2:
            smote_dict = {0: int(round(class_values[1]*imbalance[0])),
                          1: class_values[1],
                          2: int(round(class_values[1]*imbalance[1]))}
        else:
            smote_dict = {0: class_values[0],
                          1: int(round(class_values[0]*imbalance))}

        print(smote_dict)
        oversample = SMOTE(sampling_strategy=smote_dict)
        X, y = oversample.fit_resample(X, y)
        final_Mdl.fit(X, y)

    elif imbalance == "adasyn":
        class_values = y.value_counts()
        smote_dict = {0: int(round(class_values[1]*0.75)),
                      1: class_values[1],
                      2: int(round(class_values[1]*0.75))}
        ada = ADASYN(sampling_strategy=smote_dict,
                     random_state=random_seed, n_neighbors=10)
        X, y = ada.fit_resample(X, y)
        final_Mdl.fit(X, y)

    elif imbalance == "undersample":
        X, y = nr.fit_sample(X, y)
        final_Mdl.fit(X, y)

    elif imbalance == "none":
        print("FINAL MODEL HAS BEEN FITTED!")
        final_Mdl.fit(X, y)

    elif imbalance == "balanced":
        w = class_weight.compute_sample_weight("balanced", y)
        final_Mdl.fit(X, y, sample_weight=w)

    ### Feature importances ###
    importances = final_Mdl.feature_importances_
    # Sort in descending order
    indices = np.argsort(importances)[::-1]
    # Rearrange feature names so they match the sorted feature importances
    names = [feat_names[i] for i in indices]   # for sfs

    # Create plot
    plt.figure()
    plt.bar(range(X.shape[1]), importances[indices])
    plt.title("XGBoost Feature Importance")
    plt.xticks(range(X.shape[1]), names,
               fontsize=18, rotation=45, horizontalalignment="right")
    plt.yticks(fontsize=20)
    plt.bar(range(X.shape[1]), importances[indices])
    plt.savefig(path+"/{}_XGB_featureImps.png".format(condition),
                bbox_inches='tight', dpi=600)
    plt.show()

    end = time.time()
    print("Fit Time: {}".format(end - start))

    return final_Mdl, df_loop_scores


def multi_heatmap(explainer, X, num_class, order="explanation",
                  feat_values=None, display_feats=None,
                  cmap="bwr", class_names=None,
                  max_display=10, condition=None,
                  fig_path="./", showOutput=True):
    '''
    This function creates a heatmap of SHAP values, given a SHAP explainer object
    and the feature matrix to be explained. The function is primarily made up
    of the source code from the shap.plots.heatmap function, however it has been
    adjusted to accomodate multi-class models. 
    Refer to https://shap.readthedocs.io/en/latest/example_notebooks/api_examples/plots/heatmap.html
    for more info on the SHAP heatmaps.

    Function Inputs:
    ----------
    1. explainer:       SHAP explainer object
    2. X:               The independent data that you want explained 
    3. num_class:       Number of classes in model
    4. class_names:     Names of target classes 
    5. order:           Method for clustering the SHAP values
                        a.) "explanation" (default): samples are grouped based on 
                             a hierarchical clustering by their explanation similarity
                             b.) "output": samples are ordered by model output, f(x), 
                            which is shown in log odds on the line plot above the 
                            heatmap.
    6. feat_values:     Array of values used to sort the model features on the y-axis.
                        Should be equal to number of features. If not given, features
                        are sorted by their absolute magnitude SHAP value.
    7. display_feats:   Feature names to use for the plots (if they differ from the
                        feature matrix column names).
    8. cmap:            Colormap used for the heatmap. Default is 'bwr'.
    9. max_display:     Maximum number of features to display on y-axis.
    10. condition:       String used to identify dataset condition (e.g "e.coli").
                        Used to name/save plots.
    11. fig_path:       Where to save the heatmap figure. Default is './'.
    12. showOutput      Whether to show model output, f(x), in lineplot above 
                        heatmap.

    Function Outputs:
    ----------
    1. explainer:   SHAP explainer object
    2. shap_values: matrix of SHAP values
    '''
    pltFont = {"fontname": "Arial"}
    if class_names is None:
        class_names = list(range(len(num_class)))
                               
    f = []
    for class_num in range(num_class):
        feature_values = feat_values

        print("ITERATION {}".format(class_num))
        shap_values = explainer(X)[:, :, class_num]

        # define clustering method for observations
        if order == "explanation":
            instance_order = shap_values.hclust()
        elif order == "output":   # use "output" to cluster by model output
            instance_order = shap_values.sum(1)
            instance_order = instance_order.argsort.flip.values

        # define order of features on y-axis
        if feat_values is None:
            feature_values = shap_values.abs.mean(0)
            feature_values = feature_values.values
        show = True

        # sort the SHAP values matrix by rows and columns
        values = shap_values.values

        feature_order = np.argsort(-feature_values)

        xlabel = "Instances"

        if display_feats is not None:
            feature_names = np.array(display_feats)[feature_order]
        else:
            feature_names = np.array(shap_values.feature_names)[feature_order]

        values = shap_values.values[instance_order][:, feature_order]
        feature_values = feature_values[feature_order]

        # collapse
        if values.shape[1] > max_display:
            new_values = np.zeros((values.shape[0], max_display))
            new_values[:, :max_display-1] = values[:, :max_display-1]
            new_values[:, max_display-1] = values[:, max_display-1:].sum(1)
            new_feature_values = np.zeros(max_display)
            new_feature_values[:max_display-1] = feature_values[:max_display-1]
            new_feature_values[max_display -
                               1] = feature_values[max_display-1:].sum()
            feature_names = list(feature_names[:max_display])
            feature_names[-1] = "Sum of %d other features" % (
                values.shape[1] - max_display + 1)
            values = new_values
            feature_values = new_feature_values

        # define the plot size
        # cmap='coolwarm'
        plt.figure()
        row_height = 0.5
        plt.gcf().set_size_inches(8, values.shape[1] * row_height + 2.5)

        # plot the matrix of SHAP values as a heat map
        vmin = np.nanpercentile(values.flatten(), 1)
        vmax = np.nanpercentile(values.flatten(), 99)
        plt.imshow(
            values.T, aspect=0.7 * values.shape[0]/values.shape[1], interpolation="nearest", vmin=min(vmin, -vmax), vmax=max(-vmin, vmax),
            cmap=cmap)
        yticks_pos = np.arange(values.shape[1])
        yticks_labels = feature_names

        # plot f(x) above heatmap
        if showOutput:
            plt.yticks([-1.5] + list(yticks_pos),
                       ["f(x)"] + list(yticks_labels),
                       fontsize=18, **pltFont)          # for y-axis labels
            plt.ylim(values.shape[1]-0.5, -3)
            plt.xticks(fontsize=18, **pltFont)     # for x-axis ticks
            # create model output plot above heatmap
            plt.gca().xaxis.set_ticks_position('bottom')
            plt.gca().yaxis.set_ticks_position('left')
            plt.gca().spines['right'].set_visible(True)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.axhline(-1.5, color="#aaaaaa", linestyle="--", linewidth=0.5)
            fx = values.T.mean(0)
            f.append(fx)
            plt.plot(-fx/np.abs(fx).max() - 1.5, color="#000000", linewidth=1)

        else:
            plt.yticks(list(yticks_pos),
                       list(yticks_labels), fontsize=15, **pltFont)

            plt.ylim(values.shape[1]-0.5, -3)
            plt.xticks(fontsize=14, **pltFont)
            fx = values.T.mean(0)
            f.append(fx)

        # pl.colorbar()
        plt.gca().spines['left'].set_bounds(values.shape[1]-0.5, -0.5)
        plt.gca().spines['right'].set_bounds(values.shape[1]-0.5, -0.5)
        # plot feature importance bars to right of heatmap
        b = plt.barh(
            yticks_pos, (feature_values /
                         np.abs(feature_values).max()) * values.shape[0] / 20,
            0.7, align='center', color="#000000", left=values.shape[0] * 1.0 - 0.5
            #color=[colors.red_rgb if shap_values[feature_inds[i]] > 0 else colors.blue_rgb for i in range(len(y_pos))]
        )
        for v in b:
            v.set_clip_on(False)
        plt.xlim(-0.5, values.shape[0]-0.5)
        plt.xlabel(xlabel, fontsize=20, **pltFont)  # for "Instances"

        # plot colorbar
        m = cm.ScalarMappable(cmap=cmap)
        m.set_array([min(vmin, -vmax), max(-vmin, vmax)])
        cb = plt.colorbar(m, ticks=[min(vmin, -vmax), max(-vmin, vmax)], aspect=1000, fraction=0.0090, pad=0.10,
                          panchor=(0, 0.05))
        #cb.set_ticklabels([min(vmin,-vmax), max(-vmin,vmax)])
        # orig pad: -10, for colorbar label
        cb.set_label("SHAP value", size=20, labelpad=-30, **pltFont)
        # orig size: 11, for colorbar numbers
        cb.ax.tick_params(labelsize=18, length=0)
        cb.set_alpha(1)
        cb.outline.set_visible(False)
        bbox = cb.ax.get_window_extent().transformed(
            plt.gcf().dpi_scale_trans.inverted())
        cb.ax.set_aspect((bbox.height - 0.9) * 15)
        cb.ax.set_anchor((1, 0.2))
        # cb.draw_all()

        for i in [0]:
            plt.gca().get_yticklines()[i].set_visible(False)
        plt.title("{}".format(class_names[class_num]), fontsize=20, pad=0)

        # save
        plt_name = "ShapHeatmap_{}".format(class_names[class_num])
        print(plt_name)
        plt.savefig(fig_path+"/{}_{}.png".format(plt_name, condition),
                    dpi=600, bbox_inches='tight')
        plt.show()

    return 


def shapley(xgbModel, X, condition="CAROM",
              class_names=None,
              dependence=False, heatmap=True,
              display_feats=None,
              fig_path= '../figures/SHAP'):
    '''
    This function performs various analyses using the SHAP package. Given
    a classification model and the dataframe of feature values which you want
    explained, the function will output the SHAP explainer object and SHAP
    values. Additionally, SHAP summary plots, heatmaps and decision plots are
    created. 
    Refer to https://shap.readthedocs.io/en/latest/ for more info on the SHAP
    package.

    Function Inputs:
    ----------
    1. xgbModel:        XGBoost classification model
    2. X:               Feature matrix (independent data) that you want explained 
    3. condition:       String used to identify dataset condition
    4. class_names:     Names of target classes.
    5. dependence:      Whether to output SHAP dependence plots for top 3 most
                        important features.
    6. heatmap:         Whether to output SHAP value heatmap. 
    7. display_feats:   Feature names to use in plots, if they differ from the
                        column names of X.
    8. fig_path:        Where to save SHAP figure outputs. Default is '../figures/SHAP'

    Function Outputs: 
    ----------
    1. explainer:   SHAP explainer object
    2. shap_values: matrix of SHAP values
    '''

    # create directories for SHAP figures
    paths = [fig_path,
             fig_path+"/summary_plots",
             fig_path+"/dependence_plots",
             fig_path+"/heatmaps"]
    
    for path in paths:
        try:
            os.mkdir(path)
        except OSError:
            print("Directory %s failed (may already exist)" % path)
        else:
            print("Successfully created the directory %s " % path)

    # define font type for SHAP plots
    pltFont = {'fontname': 'Arial'}
    plt.rcParams.update(plt.rcParamsDefault)

    # define feature and class names
    feat_names = X.columns

    if display_feats is None:
        display_feats = feat_names

    if class_names is None:
        class_names = xgbModel.classes_
    num_class = len(class_names)

    # create SHAP explainer and get SHAP values
    explainer = shap.TreeExplainer(xgbModel,
                                   feature_perturbation='tree_path_dependent')
    X_test = X
    shap_values = explainer.shap_values(X_test)
    explainer_object = explainer(X_test)    # X_test

    # shap_interaction_values = explainer.shap_interaction_values(X_test)
    # expected_value = explainer.expected_value

    ## SHAP summary and dependence plots ##
    if num_class > 2:   # if mulit-class

        # summary plot for all classes
        plt.figure()
        shap.summary_plot(shap_values, X_test,
                          class_names=class_names,
                          feature_names=display_feats,
                          show=False)
        plt.title("SHAP Summary Plot: {}".format(
            condition), fontsize=20, **pltFont)
        plt.yticks(fontsize=18, **pltFont)
        plt.xticks(fontsize=18, **pltFont)
        plt.xlabel("mean(|SHAP value|) (average impact on model output magnitude)",
                   fontsize=20, **pltFont)
        plt.savefig(paths[1]+"/{}_MultiSummaryPlot.png".format(condition),
                    bbox_inches='tight', dpi=600)
        plt.show()

        # get order of feature importance from multi-class summary plot
        # (to be used for ordering class-specific summary plots)
        my_order = explainer_object[:, :, 0].abs.mean(
            0)+explainer_object[:, :, 1].abs.mean(0)+explainer_object[:, :, 2].abs.mean(0)

        # loop through classes for class-specific summary and dependence plots
        for which_class in range(num_class):

            print("Current class: ", which_class)

            # summary single class (shap.summary_plot)
            shap.plots.beeswarm(explainer_object[:, :, which_class],
                                order=my_order,
                                max_display=len(feat_names),
                                color_bar=False,
                                show=False)
            plt.title("{}".format(
                class_names[which_class]), fontsize=20, **pltFont)
            plt.yticks(fontsize=18, **pltFont)
            plt.xticks(fontsize=18, **pltFont)
            plt.xlabel("SHAP Value (impact on model output)",
                       fontsize=20, **pltFont)
            # make our own color bar so that we can adjust font/label sizes
            cm1 = mcol.LinearSegmentedColormap.from_list(
                "MyCmapName", ["#4d73ff", "#ff1303"])
            cnorm = mcol.Normalize(vmin=0, vmax=1)
            m = pltcm.ScalarMappable(norm=cnorm, cmap=cm1)
            m.set_array([0, 1])
            cb = plt.colorbar(m, ticks=[0, 1], aspect=1000)
            cb.set_ticklabels(["Low", "High"])
            cb.set_label("Feature Value", size=18, labelpad=-10)
            cb.ax.tick_params(labelsize=18, length=0)
            cb.set_alpha(1)
            cb.outline.set_visible(False)
            bbox = cb.ax.get_window_extent().transformed(
                plt.gcf().dpi_scale_trans.inverted())
            cb.ax.set_aspect((bbox.height - 0.9) * 20)
            plt.savefig(paths[1]+"/{}_{}_SingleSummaryPlot.png".format(condition, class_names[which_class]),
                        dpi=600, bbox_inches='tight')
            plt.show()

            # dependence plots (only plot for top 3 important feats)
            vals = np.abs(shap_values[which_class]).mean(0)
            # Sort feature importances in descending order
            indices = np.argsort(vals)[::-1]
            feat_names = X_test.columns
            sorted_names = [display_feats[ind] for ind in indices]
            if dependence:
                for i in range(3):
                    shap.dependence_plot(ind=sorted_names[i],
                                         shap_values=shap_values[which_class],
                                         features=X_test,
                                         feature_names=display_feats,
                                         interaction_index="auto",
                                         x_jitter=1,
                                         show=False)  # *****
                    # plt.title("Dependence Plot")
                    plt.savefig(paths[2]+"/{}_{}_{}_dependencePlot.png".format(
                        condition, class_names[which_class], sorted_names[i]))
                    plt.show()

        if heatmap:
            multi_heatmap(explainer, X_test,
                          num_class, order="output",
                          class_names=class_names,
                          condition=condition,
                          display_feats=display_feats,
                          max_display=len(feat_names), fig_path=paths[3])

    elif num_class == 2:   # binary problem

        # summary plot for 'positive' class
        plt.figure()
        shap.summary_plot(shap_values, X_test,
                          feature_names=display_feats, show=False)
        plt.title("SHAP Summary Plot: {}".format(condition), fontsize=15)
        plt.show()
        plt.savefig(paths[1]+"/{}_SummaryPlot.png".format(condition),
                    bbox_inches='tight', dpi=600)

        if dependence:
            shap.dependence_plot("rank(0)", shap_values, X_test, show=False)
            plt.title("Dependence Plot", fontsize=15)
            plt.savefig(paths[2]+"/{}_DependencePlot.png".format(condition),
                        dpi=600)
            plt.show()

        if heatmap:
            # limit size of explainer object (shap.plots.heatmap seems to struggle
            # with very large datasets)
            if len(explainer_object) > 2000:
                explainer_object = explainer(X_test.sample(2000))

            shap.plots.heatmap(explainer_object,
                               max_display=len(feat_names))
            plt.savefig(paths[3]+"/{}_ShapHeatmap.png".format(condition),
                        dpi=600)

    return explainer, shap_values


def select_genes(X, y, all_genes, select_genes,
                  model, explainer,
                  class_names=None, display_features=None,
                  condition="PredictGenes",
                  fig_path="../figures/predictGenes"):
    '''
    This function is used to analyze a model's predictions on specific genes
    of interest. It is assumed that the true class is known for the dataset.

    Function Inputs:
    ----------
    1. X:                   Feature matrix
    2. y:                   Target variable array
    3. all_genes:           String array of all genes corresponding to the rows
                             in the X and y datasets.              
    4. select_ganes:        String or string array of gene names to be analyzed
    5. model:             Classifier model
    6. explainer:           SHAP explainer object corresponding to model
    7. class_names:         String array of class names
    8. condition:           String of dataset condition (for naming plots) 
    9. display_features:    Feature names to display in plots, if they differ
                            from the column names of X.
   10. fig_path:            Where to save figures. Default is "../figures/predictGenes"

    Function Outputs: 
    ----------
    1. SHAP decision plots - shows the prediction path for all instances of the
       gene of interest, with a separate plot for each class.
    2. SHAP mulitoutput decision plot - shows the prediction path for a single 
       instance of the gene of interest, with all classes are displayed on same
       plot.

      All plots are saved to the 'figures/predictGenes' folder.
    '''
    # make folder for figures
    path = fig_path
    try:
        os.mkdir(path)
    except OSError:
        print("Directory %s failed (may already exist)" % path)
    else:
        print("Successfully created the directory %s " % path)

    pltFont = {'fontname': 'Arial'}
    plt.rcParams.update(plt.rcParamsDefault)

    # get feature names and number of classes
    feature_names = X.columns
    # feat_names_list = feature_names.tolist()
    if display_features is None:
        display_features = list(feature_names)
    
    if class_names is None:
        class_names = model.classes_.astype(str)
        
    num_class = len(y.unique())

    # transform class integers to [0,1,2]
    le = preprocessing.LabelEncoder()
    le.fit(y)
    y = pd.Series(le.transform(y))

    # get indices of gene of interest
    i_genes = []
    for gene in select_genes:
        bool_list = all_genes["genes"].eq(gene)
        i_gene = list(compress(range(len(bool_list)), bool_list))
        i_genes.extend(i_gene)
        
    if len(i_genes)==0:
        print("GENES NOT FOUND!")
    else:
        print("i_genes: /n", i_genes, "/n")
        # get X, y and y_pred for genes of interest
        X_test = X.loc[X.index.isin(i_genes), feature_names]
        print("X_test: /n", X_test, "/n")
        y_test = y[y.index.isin(i_genes)]
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
    
        # create dataframe showing y_test and y_pred
        test_index = X_test.index.tolist()
        test_genes = all_genes.loc[test_index, "genes"]
        test_rxns = all_genes.loc[test_index, "reaction"]
        data = {'Test Genes': test_genes,
                'Test Rxns': test_rxns,
                'y_test': y_test,
                'y_pred': y_pred}
        df = pd.DataFrame(
            data, columns=['Test Genes', 'Test Rxns', 'y_test', 'y_pred'])
        print(df)
    
        # SHAP decision plot
        expected_value = explainer.expected_value
        print(expected_value)
    
        for gene in select_genes:
    
            bool_genes = df["Test Genes"] == gene   # get rows for current gene
    
            features = X_test[bool_genes]   # get features for current gene
    
            # y_pred (from XGBoost mdl) and y_test for current gene
            y_pred_select = y_pred[bool_genes]
            y_test_select = y_test[bool_genes]
    
            # probabilities for current gene prediction
            y_proba = model.predict_proba(features)
            print("Probabilities:")
            print(y_proba)
    
            # log odds for current gene prediction
            logodds = model.predict(features, output_margin=True)
            print("Log odds:")
            print(logodds)
    
            # mis-classified genes (to be used for highlight, if desired)
            misclass_genes = y_test_select != y_pred_select
    
            # we will create decision plot for each class, so loop through classes
            for j in y.unique()[::-1]:
                # ID genes of current class in y_test (to be used for highlighting)
                class_genes = y_test_select == j
    
                # get shap values of specified observations
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    # j starts with -1, so add 1 to get index 0
                    shap_values_decision = explainer.shap_values(features)[j]
                    shap_interaction_values = explainer.shap_interaction_values(features)[
                        j]
                if isinstance(shap_interaction_values, list):
                    shap_interaction_values = shap_interaction_values
    
                # create decision plot
                shap.decision_plot(expected_value[j], shap_values_decision,
                                   features,
                                   highlight=class_genes,
                                   feature_names=display_features,
                                   show=False)
                plt.title("SHAP Decision Plot: {}, {}".format(
                    gene, class_names[j]), fontsize=15)
                plt.savefig(path+"/{}_{}_{}DecisionPlot.png".format(condition, gene, class_names[j]),
                            bbox_inches='tight', dpi=600)
                plt.show()
                
    
        ### SHAP multi-output decision plot ###
    
        # function create legend labels using class name and log odds value
        def class_labels(row_index):
            return [f'{j} ({logodds[row_index, i].round(2):.2f})' for i, j in enumerate(class_names)]
    
        for gene in select_genes:
            # ID rows with current gene and correct classification
            bool_genes = (df["Test Genes"] == gene)
                # & (df["y_test"] == df["y_pred"])
    
            # if at least 1 gene present
            if sum(bool_genes) > 0:
                if sum(bool_genes) < 3:
                    rows = sum(bool_genes)
                else:
                    rows = 3
    
                features = X_test[bool_genes]   # get features for above rows
                rxns = df.loc[bool_genes, "Test Rxns"]
                print("REACTIONS: ", rxns)
                classifications = df.y_test[bool_genes]==df.y_pred[bool_genes]
                # get shap values for select features
                shap_values = explainer.shap_values(features)
                # shap_explainer = explainer(features)
    
                # get log odds for select genes
                logodds = model.predict(features, output_margin=True)
                print("{} Log odds: ".format(gene))
                print(logodds)
    
                # create multi-output decision plot for first 2 observations (w/ correct classification)
                for row in range(rows):
                    rxn = rxns.iloc[row]
                    classification_bool=classifications.iloc[row]
                    if classification_bool:
                        classification="TP"
                    else:
                        classification="FN"
                        
                    plt.figure(figsize=(8, 6))
                    shap.multioutput_decision_plot(expected_value, shap_values,
                                                   row_index=row,
                                                   feature_names=display_features,
                                                   highlight=[np.argmax(logodds[row])],
                                                   legend_labels=None,
                                                   show=False)
                    # fix line colors and weights
                    num_lines = len(plt.gca().lines)
                    num_classes = len(class_names)
                    for line, color in zip(plt.gca().lines[num_lines-num_classes:num_lines],
                                           ["#0070C0", "#FFD55A", "#6DD47E"]):
                        line.set_linewidth(4)
                        line.set_color(color)
                    # fix legend
                    plt.legend(handles=plt.gca().lines[num_lines-num_classes:num_lines],
                               labels=class_labels(row),
                               loc="lower right", fontsize=16)
                    plt.title("Gene-Rxn: {}-{}".format(gene, rxn),
                              fontsize=20, **pltFont)
                    plt.xticks(fontsize=20, **pltFont)
                    plt.yticks(fontsize=20, **pltFont)
                    plt.xlabel("Model output value", fontsize=20, **pltFont)
    
                    regType = class_names[np.argmax(logodds[row])]
                    plt.savefig(path+"/{}_{}-{}_{}{}_MultiOutputPlot.png".format(
                        condition, gene, rxn, regType, classification),
                        bbox_inches='tight', dpi=600)
                    plt.show()


def decisionTree(X, y, class_names,
                 weighting="none", weights=None,
                 pruneLevel=0, condition="Condition",
                 make_viz=False, random_seed=123,
                 fig_path="../figures/decision_trees/", sub_path=""):
    '''
    Function Inputs:
    ----------
    1. X:            Features matrix
    2. y:            Target variable array
    3. class_names:  String array of class names
    4. weighting:    Options for handling class imbalance
                     a.) "none" (default): no class weights or sampling applied
                     b.) "balanced":       inverse class proportions
                                           used to assign class weights
                     c.) "smote":          SMOTE over-sampling applied 
                     d.) "tuned":          weights are tuned via cross-validation
                     e.) list of floats:   floats are used to determine ratio for
                                           SMOTE. Assumed classes 0 and 2 are minority.
                                           (e.g. [0.5 0.75] = sample class 0 to 50%
                                                  of class 1, class 2 to 75% of class 1)
    5. weights       Dictionary of weights to use with the "tuned" weighting
                     option   .
    6. pruneLevel    Integer, designating the minimum number of observations
                     in a leaf for it to be pruned.
    7. condition:    String of dataset condition (for naming plots/files)
    8. make_viz:     Whether to make additional tree figure using dtree_viz package.
    9. random_seed:  Random seed for tuning decision trees.
   10. fig_path:     Path for saving decision tree figures. Default is "../figures/decision_trees"
   11. sub_path:     Sub-folder name for keeping figures organized. If none is
                     given, all  figures saved in fig_path. 


    Function Outputs: 
    ----------
    Decision tree plots are saved to the 'figures/decision_trees' folder.
'''
    # define path name for saving trees
    path = fig_path+sub_path
        
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

    # if make_viz is True:
    #     viz_path = path+"dtreeviz"
    #     try:
    #         os.mkdir(viz_path)
    #     except OSError:
    #         print("Creation of the directory %s failed" % viz_path)
    #     else:
    #         print("Successfully created the directory %s " % viz_path)

    # create Dtrees at multiple depths
    treeDict_VarDepths = {}

    param_dist = {"min_samples_leaf": [1, 3, 5, 10, 20],  # default=1, range:1-20
                  # default=2, range:1-40
                  "min_samples_split": [2, 3, 5, 10, 25],
                  "criterion": ["gini", "entropy"],
                  "max_features": ["sqrt", "log2", None]}

    # define weights if not given
    if weights is None:
        weights = [{-1: 2, 0: 1, 1: 2}, {-1: 4, 0: 1, 1: 4},
                   {-1: 4, 0: 1, 1: 2}, {-1: 10, 0: 1, 1: 5}]

    feats = X.columns

    for i, depth in enumerate([3, 4]):

        if weighting == "tuned":
            treeDict_VarWeights = {}
            scores = []
            for count, weight in enumerate(weights):

                # Instantiate a Decision Tree classifier: tree
                dtree = DecisionTreeClassifier(class_weight=weight,
                                               max_depth=depth,
                                               random_state=random_seed)

                # Instantiate the RandomizedSearchCV object: tree_cv
                tree_cv = RandomizedSearchCV(dtree, param_dist,
                                             n_iter=30, cv=5,
                                             scoring="f1_macro",
                                             random_state=random_seed)

                # Fit it to the data
                tree_cv.fit(X, y)  # ,sample_weight=w_array
                treeDict_VarWeights[count] = tree_cv
                scores.append(tree_cv.best_score_)
                print("Best score is {}".format(tree_cv.best_score_))

            maxpos = scores.index(max(scores))
            print(treeDict_VarWeights[maxpos].best_params_)
            tree_clf = treeDict_VarWeights[maxpos].best_estimator_

        elif weighting == "balanced":
            dtree = DecisionTreeClassifier(class_weight='balanced',
                                           max_depth=depth,
                                           random_state=random_seed)
            tree_cv = RandomizedSearchCV(dtree, param_dist,
                                         n_iter=30, cv=5,
                                         scoring="f1_macro",
                                         random_state=random_seed)
            tree_cv.fit(X, y,
                        sample_weight=class_weight.compute_sample_weight("balanced", y))
            tree_clf = tree_cv.best_estimator_

        elif weighting == "smote":
            dtree = DecisionTreeClassifier(max_depth=depth,
                                           random_state=random_seed)

            oversample = SMOTE()
            XtrainRes, ytrainRes = oversample.fit_resample(X, y)

            tree_cv = RandomizedSearchCV(dtree, param_dist,
                                         n_iter=30, cv=5,
                                         scoring="f1_macro",
                                         random_state=random_seed)
            tree_cv.fit(XtrainRes, ytrainRes)
            tree_clf = tree_cv.best_estimator_

        elif isinstance(weighting, (list, float)):
            dtree = DecisionTreeClassifier(max_depth=depth,
                                           random_state=random_seed)

            class_values = y.value_counts()
            smote_dict = {-1: int(round(class_values[0]*weighting[0])),
                          0: class_values[0],
                          1: int(round(class_values[0]*weighting[1]))}
            print(smote_dict)
            oversample = SMOTE(sampling_strategy=smote_dict)
            XtrainRes, ytrainRes = oversample.fit_resample(X, y)

            tree_cv = RandomizedSearchCV(dtree, param_dist,
                                         n_iter=30, cv=5,
                                         scoring="f1_macro",
                                         random_state=random_seed)
            tree_cv.fit(XtrainRes, ytrainRes)
            tree_clf = tree_cv.best_estimator_

        elif weighting == "none":
            dtree = DecisionTreeClassifier(max_depth=depth,
                                           random_state=random_seed)
            tree_cv = RandomizedSearchCV(dtree, param_dist,
                                         n_iter=30, cv=5,
                                         scoring="f1_macro",
                                         random_state=random_seed)
            tree_cv.fit(X, y)
            tree_clf = tree_cv.best_estimator_

        # get rid of redundant splits
        tree_clf = prune(tree_clf)

        # evaluate model w/ resubstitution
        y_predDT = tree_clf.predict(X)
        mcc = matthews_corrcoef(y, y_predDT)
        print(mcc)

        # prune tree and re-evaluate
        prunedTree_clf = copy.deepcopy(tree_clf)  # create copy of DT to prune
        prune_index(prunedTree_clf.tree_, 0, pruneLevel)   # run prune function
        prunedTree_clf = prune(prunedTree_clf)  # get rid of unnecessary splits

        # store Dtree model
        treeDict_VarDepths[i] = prunedTree_clf

        # evaluate model w/ resubstitution
        yPredPruned = prunedTree_clf.predict(X)
        mccPruned = matthews_corrcoef(y, yPredPruned)
        print("Pruned tree MCC: {}".format(mccPruned))

        # save tree figure
        file_name = "/{}_MaxDepth{}.png".format(
            condition, depth)

        fig = plt.figure(figsize=(40, 20))
        _ = tree.plot_tree(prunedTree_clf,
                           feature_names=feats,
                           class_names=class_names,
                           fontsize=14,
                           impurity=False,
                           filled=True)

        plt.title("{} \nMAX DEPTH: {}\n MCC: {:.3f}".format(
            condition, depth, mccPruned), fontsize=36)
        fig.savefig(path+file_name)  # DO NOT USE DPI !!! ###

        # if make_viz is True:
        #     file_name_viz = "/{}_MaxDepth{}.svg".format(
        #         condition, depth)
        #     viz = dtreeviz(prunedTree_clf, X, y,
        #                    target_name="PTM",
        #                    feature_names=feats,
        #                    class_names=class_names,
        #                    label_fontsize=14,
        #                    ticks_fontsize=12,
        #                    histtype="barstacked")  # barstacked, bar, stripped
        #     viz.save(viz_path+file_name_viz)

        cm = confusion_matrix(y, yPredPruned)
        print(cm)
        path = fig_path+"/figures/decision_trees/{}".format(sub_path)

def make_predictions(mdl, X_test, gene_reactions,condition="CAROM",
                class_names=None, display_feats=None,
                y_test=None, X_train=None, y_train=None,
                pos_label=None,
                confusion_mat=True, bar=False,
                pairwise=False, boxplot=False,
                explainer=None, save=True,
                fig_path="../figures/mdl_predict/"):
    '''
    Function Inputs:
    ----------
    1. mdl:             Classifier model
    2. X_test:               Features matrix used for predictions
    3. condition:       string of dataset condition (for naming plots/files)
    4. gene_reactions:  Dataframe with some type of IDs for observations in X_test, such as
                        gene and reaction names. Used to output names of predictions
                        for each class.
                        Ex: df[['genes','reactions']]
    5. class_names:     Target variable class names
    6. display_feats:   Feature names to display if different than X_test.columns
    7. y_test:               True values of target variable. If given, output will
                        include figures related to classification performance.
                        If NOT given, model will only return predictions. 
    8. X_train:         Feature matrix used to train mdl. Needed for multiclass ROC plots.
    9. y_train.         Target array used to train mdl. Needed for multiclass ROC plots.
    10. pos_label:      Integer designating the positive class.
    11. confusion_mat:   Option to output classification confusion matrix
                        (default=True).
    12. bar:             Option to output bar graph with classification scores
                        (default=False).
    13. pairwise:        Option to output pairwise plot for top 5 most important
                        features (default=False).
    14. boxplot:        Option to output matrix of feature boxplots grouped by 
                        features classification group (default=False).
    15. explainer:      SHAP explainer object (default=None). If given, several
                        plots are produced with the SHAP package.  
    16. save:           Whether to save model predictions to csv files.
    17. fig_path:       Folder name for saved figures. Default is "../figures/mdl_predict/"

    Function Outputs:
    ----------
    *** If 'y' is provided:
    1. scores:          model's classification scores
    2. acetylGenesPred: list of genes/reactions predicted to be Acetyl
    3. phosGenesPred:   list of genes/reactions predicted to be Phos
    4. ypred:           array of model class predictions as integers 

    *** If 'y' is NOT provided:
    1. acetylGenesPred: list of genes/reactions predicted to be Acetyl
    2. phosGenesPred:   list of genes/reactions predicted to be Phos
    3. ypred:           array of model class predictions as integers 

    '''

    # make folder for output figures
    path = fig_path
    try:
        os.makedirs(path)
    except OSError:
        print("Creation of directory %s failed (may already exist)" % path)

    # set font for figures
    pltFont = {'fontname': 'Arial'}

    # define feature names and # classes
    feat_names = X_test.columns

    # reset indices
    X_test = X_test.reset_index(drop=True)
    gene_reactions = gene_reactions.reset_index(drop=True)

    # get model predictions and probabilities
    ypred = mdl.predict(X_test)
    print(Counter(ypred))
    yproba = mdl.predict_proba(X_test)

    num_pred = yproba.shape[1]   # number of classes in MODEL
    # number of class that received a prediction
    num_pred_major = len(np.unique(ypred))

    if class_names is None:
        class_names = []
        for cl in np.sort(pd.Series(ypred).unique()):
            class_names.append(np.array2string(cl))

    if num_pred_major == len(class_names):
        # if all model classes received a prediction, use all class names
        my_classes = class_names
    else:
        # else only use class names that received a prediction
        my_classes = []
        for i in np.sort(np.unique(ypred)):
            my_classes.append(class_names[i])

    print("MY CLASSES: ", my_classes)

    # if y_test is given, perform following analyses of
    # model's classification performance:
    if y_test is not None:
        # transform Target classes to 0, 1, 2
        y_test = y_test.reset_index(drop=True)
        le = preprocessing.LabelEncoder()
        le.fit(y_test)
        y_test = pd.Series(le.transform(y_test))

        le.fit(y_train)
        y_train = pd.Series(le.transform(y_train))

        cm = confusion_matrix(y_test, ypred)
        print(cm)
        num_class = len(cm)  # size of CM

        path2 = '../results'
        try:
            os.makedirs(path2)
        except OSError:
            print("Creation of directory %s failed (may already exist)" % path2)

        if num_class > 2:
            print("MULTI-CLASS PROBLEM!")
            # write classification results to CSV
            if save:
                for class_num, class_name in zip([0, 2], ["Phosphorylation", "Acetylation"]):

                    genes_FP = gene_reactions.iloc[np.where(
                        (y_test != class_num) & (ypred == class_num))]
                    if len(genes_FP) > 0:
                        genes_FP.to_csv('../results/{}_{}_FalsePos_GeneRxns.csv'.format(condition, class_name),
                                        index=False)

                    genes_FN = gene_reactions.iloc[np.where(
                        (y_test == class_num) & (ypred != class_num))]
                    if len(genes_FN) > 0:
                        genes_FN.to_csv('../results/{}_{}_FalseNeg_GeneRxns.csv'.format(condition, class_name),
                                        index=False)

                    genes_TP = gene_reactions.iloc[np.where(
                        (y_test == class_num) & (ypred == class_num))]
                    if len(genes_TP) > 0:
                        genes_TP.to_csv('../results/{}_{}_TruePos_GeneRxns.csv'.format(condition, class_name),
                                        index=False)

            # calculate classification scores based on number of classes
            if pos_label is not None:
                # we have a 3x3 confusion mat, but only interested in class 0
                TP = cm[0, 0]
                FP = cm[1, 0]
                TN = sum(cm[1, 1:])
                FN = sum(cm[0, 1:])
                accuracy = accuracy_score(y_test, ypred)
                precision = TP/(TP+FP)
                recall = TP/(TP+FN)
                f1 = 2*(recall*precision)/(recall+precision)
                mcc = (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
                r = np.corrcoef(y_test, ypred)[0, 1]
            else:
                # we have a 3x3 confusion matrix and are interested in all classes
                accuracy = accuracy_score(y_test, ypred)
                f1 = f1_score(y_test, ypred, average="macro")
                recall = recall_score(y_test, ypred, average="macro")
                precision = precision_score(y_test, ypred, average="macro")
                mcc = matthews_corrcoef(y_test, ypred)
                r = np.corrcoef(y_test, ypred)[0, 1]

            [mean_auc, fig] = plot_roc(mdl,
                                       X_train=X_train, y_train=y_train,
                                       X_test=X_test, y_test=y_test,
                                       class_names=class_names,
                                       pos_class=pos_label,
                                       figsize=(8, 6),
                                       show=True)
            fig.savefig(path+"/{}_ROCcurve.png".format(condition),
                        bbox_inches='tight', dpi=600)
        else:
            # confusion matrix is 2x2
            print("BINARY PROBLEM!")
            if pos_label is None:
                pos_label = 0

            # write classification results to CSV
            if save:
                genes_FP = gene_reactions.iloc[np.where(
                    (y_test != pos_label) & (ypred == pos_label))]
                if len(genes_FP) > 0:
                    genes_FP.to_csv('../results/{}_{}_FalsePos_GeneRxns.csv'.format(condition, class_names[1]),
                                    index=False)

                genes_FN = gene_reactions.iloc[np.where(
                    (y_test == pos_label) & (ypred != pos_label))]
                if len(genes_FN) > 0:
                    genes_FN.to_csv('../results/{}_{}_FalseNeg_GeneRxns.csv'.format(condition, class_names[1]),
                                    index=False)

                genes_TP = gene_reactions.iloc[np.where(
                    (y_test == pos_label) & (ypred == pos_label))]
                if len(genes_TP) > 0:
                    genes_TP.to_csv('../results/{}_{}_TruePos_GeneRxns.csv'.format(condition, class_names[1]),
                                    index=False)
            # calculate classification scores
            accuracy = accuracy_score(y_test, ypred)
            f1 = f1_score(y_test, ypred, average="binary", pos_label=pos_label)
            recall = recall_score(
                y_test, ypred, average="binary", pos_label=pos_label)
            precision = precision_score(
                y_test, ypred, average="binary", pos_label=pos_label)
            mcc = matthews_corrcoef(y_test, ypred)
            r = np.corrcoef(y_test, ypred)[0, 1]

            # AUC
            if num_pred == 2:  # only 2 classes in MODEL
                preds = yproba[:, pos_label]
                fpr, tpr, threshold = roc_curve(y_test, preds)
                mean_auc = auc(fpr, tpr)

                # plot
                plt.figure()
                plt.title('ROC ROC Curve')
                plt.plot(fpr, tpr, 'b', label='AUC = %0.3f' % mean_auc)
                plt.legend(loc='lower right')
                plt.plot([0, 1], [0, 1], 'r--')
                plt.xlim([0, 1])
                plt.ylim([0, 1])
                plt.ylabel('True Positive Rate')
                plt.xlabel('False Positive Rate')
                plt.savefig(path+"/{}_ROCcurve.png".format(condition),
                            bbox_inches='tight', dpi=600)
                plt.show()

            else:  # 3 classes in MODEL, but only 2 received predictions
                [mean_auc, fig] = plot_roc(mdl,
                                           X_train=X_train, y_train=y_train,
                                           X_test=X_test, y_test=y_test,
                                           class_names=class_names,
                                           pos_class=pos_label,
                                           figsize=(8, 6),
                                           show=True)

        scores = [accuracy, recall, precision, f1, mcc, mean_auc, r]
        score_names = ['Accuracy', 'Recall',
                       'Precision', 'F1', 'MCC', 'AUC', 'R']
        df_scores = pd.DataFrame(data=scores,
                                 index=score_names,
                                 columns=["Value"])

        # confusion matrix figure
        if confusion_mat is True:
            ax = make_confusion_matrix(cf=cm,
                                       y_true=y_test, y_pred=ypred,
                                       figsize=(8, 6),
                                       categories=my_classes,
                                       xyplotlabels=True,
                                       sum_stats=False,
                                       cbar=False)
            # ax.yaxis.label.set_fontsize(24)
            plt.ylabel("Experimental Labels", fontsize=24)
            plt.xlabel("Predicted Labels", fontsize=24)
            plt.savefig(path+"/{}_confusionMat.png".format(condition),
                        bbox_inches='tight', dpi=600)
            plt.show()

        # score bar graph
        if bar is True:
            plt.rcParams.update(plt.rcParamsDefault)
            fig, ax = plt.subplots(figsize=(8, 6))

            ax.bar(score_names, scores,
                   align='center',
                   alpha=0.5,
                   ecolor='black',
                   capsize=10,
                   width=0.8)
            ax.set_ylim([0, 1.0])
            ax.set_xticklabels(score_names,
                               rotation=45, ha="right",
                               rotation_mode="anchor")
            ax.tick_params(axis='both', which='major', labelsize=24)
            ax.yaxis.grid()
            plt.tight_layout()
            plt.savefig(path+"/{}_ScoresBarGraph.png".format(condition),
                        bbox_inches='tight', dpi=600)

        if pairwise is True and num_class > 2:
            # Sort feature importances in descending order
            indices = np.argsort(mdl.feature_importances_)[::-1]
            # Rearrange feature names
            names = [feat_names[i] for i in indices]

            # create pairwise plot for each PTM class
            for class_num, class_name in zip([0, 2], ["Phos", "Acetyl"]):
                if sum(y_test == class_num) > 0:
                    # get X_test for DEG rows
                    df_deg = X_test.loc[y_test == class_num]
                    # get y_test for Phos rows
                    y2 = y_test[y_test == class_num]
                    # get ypred for Phos rows
                    ypred2 = ypred[y_test == class_num]
                    # get classification results
                    df_deg['Correct'] = y2 == ypred2

                    # get 5 top feats
                    impFeats = list(names[0:5])
                    impFeats.append("Correct")
                    print("Num correct: {} ".format(sum(df_deg.Correct)))

                    # create pairwise plot using top 5 features
                    sns.set(font_scale=2)
                    plt.figure(figsize=(8, 6))
                    sns.pairplot(df_deg[impFeats],
                                 hue="Correct", hue_order=[False, True],
                                 plot_kws={'s': 70})
                    plt.savefig(path+"/{}_pairwise_Predict{}.png".format(condition, class_name),
                                bbox_inches='tight', dpi=600)
                    plt.show()

        if boxplot is True and num_class > 2:
            # create boxplot for each PTM class
            # grouped by classification label (e.g. True Positive)
            for class_num, class_name in zip([0, 2], ["Phos", "Acetyl"]):
                if sum(y_test == class_num) > 0:

                    # assign line colors based on classification
                    classification_groups = np.where((y_test == class_num) & (ypred == class_num), 'TP',
                                                     np.where((y_test != class_num) & (ypred != class_num), 'TN',
                                                              np.where((y_test == class_num) & (ypred != class_num), 'FN',
                                                                       'FP')))
                    X_temp = X_test.copy()
                    X_temp['classification'] = classification_groups

                    numeric_feats = X_test.select_dtypes(include='float64').columns
                    sns.set()
                    labels = ["TP", "FP", "TN", "FN"]

                    f, axs = plt.subplots(3, 4, figsize=(8, 6))
                    for i, ax in enumerate(axs.reshape(-1)):
                        sns.boxplot(y_test=numeric_feats[i], x="classification", data=X_temp,
                                    ax=ax, order=labels)
                        # ax.set_ylabel(str(i))
                        ax.set_xlabel('')   # remove x-axis label
                        ax.set_ylabel(numeric_feats[i], fontsize=16, **pltFont)
                        ax.set_xticklabels(labels, rotation=45, ha="center")
                        ax.tick_params(axis='both', which='major',
                                       labelsize=14)
                    plt.tight_layout()
                    plt.savefig(path+"/{}_Boxplot_{}True.png".format(condition, class_name),
                                bbox_inches='tight', dpi=600)
                    plt.show()

        if explainer and num_class > 2:

            expected_value = explainer.expected_value

            # decision plot for ~50 random observations. Repeat for each PTM class.
            for class_num, class_name in zip([0, 2], ["Phosphorylation", "Acetylation"]):

                if sum(y_test == class_num) > 0:
                    print("CURRENT CLASS: {}, COUNT = {}".format(
                        class_name, sum(y_test == class_num)))

                    yclass = np.where((y_test == class_num) & (ypred == class_num), 'TP',  # TP
                                      np.where((y_test != class_num) & (ypred != class_num), 'TN',  # TN
                                               np.where((y_test == class_num) & (ypred != class_num), 'FN',  # FN
                                                        'FP')))  # FP

                    # get features for 50 samples and find those misclassified
                    X_temp = X_test.copy()
                    X_temp["classification"] = yclass
                    X_temp2 = X_temp.groupby("classification").sample(
                        n=10, replace=True, random_state=123)

                    # assign line colors based on classification
                    ycol = np.where(X_temp2.classification == "TP", 'blue',  # TP
                                    np.where(X_temp2.classification == "TN", 'red',  # TN
                                             np.where(X_temp2.classification == "FN", 'darkred',  # FN
                                                      'deepskyblue')))  # FP

                    features = X_temp2[feat_names]
                    misclass = (X_temp2.classification == "FP") | (
                        X_temp2.classification == "FN")

                    # get shap values of specified observations
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        shap_values_decision = explainer.shap_values(features)[
                            class_num]
                    #     shap_interaction_values = explainer.shap_interaction_values(features)[class_num]
                    # if isinstance(shap_interaction_values, list):
                    #     shap_interaction_values = shap_interaction_values

                    # create decision plot
                    plt.rcParams.update(plt.rcParamsDefault)
                    f1 = plt.figure()
                    shap.decision_plot(expected_value[class_num],
                                       shap_values_decision,  # shap_interaction_values
                                       features,
                                       highlight=misclass,
                                       color_bar=False,
                                       legend_labels=None,
                                       feature_names=display_feats,
                                       feature_order='hclust',
                                       show=False)
                    plt.xlabel("Model output value", fontsize=20, **pltFont)
                    plt.yticks(fontsize=18, **pltFont)
                    plt.xticks(fontsize=18, **pltFont)
                    plt.title("Decision Plot: {}".format(class_name),
                              fontsize=20, **pltFont)

                    # fix line colors and weights
                    num_lines = len(plt.gca().lines)
                    for line, color in zip(plt.gca().lines[len(feat_names):num_lines],
                                           ycol):
                        line.set_linewidth(2)
                        line.set_color(color)

                    # create legend
                    colors = ['blue', 'red', 'darkred', 'deepskyblue']
                    styles = ['-', '-', '--', '--']
                    lines = [Line2D([0], [0], color=c, linewidth=3, linestyle=s)
                             for c, s in zip(colors, styles)]
                    labels = ['TP', 'TN', 'FN', 'FP']
                    # save fig
                    plt.legend(lines, labels,
                               fontsize=15, loc='lower right')
                    plt.savefig(path+"/{}_SHAPDecisionPlot_{}.png".format(condition, class_name),
                                bbox_inches='tight', dpi=600)
                    plt.show()

                    # create decision and summary plots for TP/FP observations
                    for class_group in (["TP", "FP"]):
                        if sum(X_temp.classification == class_group) > 0:

                            # get true/false positive genes
                            X_group = X_temp[X_temp.classification ==
                                             class_group][feat_names]
                            if class_group == "TP":
                                title = "True Positives"
                            elif class_group == "FP":
                                title = "False Positives"

                            # get shap values for TP/FP genes
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore")
                                shap_values_decision = explainer.shap_values(X_group)[
                                    class_num]
                                shap_interaction_values = explainer.shap_interaction_values(X_group)[
                                    class_num]
                            if isinstance(shap_interaction_values, list):
                                shap_interaction_values = shap_interaction_values

                            # decision plot for TP/FP genes
                            plt.rcParams.update(plt.rcParamsDefault)
                            f1 = plt.figure()
                            shap.decision_plot(expected_value[class_num],
                                               shap_values_decision,
                                               X_group,
                                               color_bar=True,
                                               legend_labels=None,
                                               feature_order='hclust',
                                               feature_names=display_feats,
                                               show=False)
                            plt.title("Decision Plot: {} {}".format(class_name, title),
                                      fontsize=20, **pltFont)
                            plt.yticks(fontsize=18, **pltFont)
                            plt.xticks(fontsize=18, **pltFont)
                            plt.xlabel("Model output value",
                                       fontsize=20, **pltFont)

                            plt.savefig(path+"/{}_ShapDecisionPlot_{}_{}.png".format(
                                condition, class_name, class_group),
                                bbox_inches='tight', dpi=600)
                            plt.show()

                            # summary plot for TP/FP genes
                            shap_values = explainer.shap_values(X_group)
                            plt.figure()
                            shap.summary_plot(shap_values[class_num], X_group,
                                              color_bar=False,
                                              feature_names=display_feats,
                                              show=False)
                            plt.title("Summary Plot: {} {}".format(class_name, title),
                                      fontsize=20, **pltFont)
                            plt.yticks(fontsize=18, **pltFont)
                            plt.xticks(fontsize=18, **pltFont)
                            plt.xlabel(
                                "SHAP Value (impact on model output)", fontsize=20, **pltFont)
                            # make our own color bar so that we can adjust font/label sizes
                            cm1 = mcol.LinearSegmentedColormap.from_list(
                                "MyCmapName", ["#4d73ff", "#ff1303"])
                            cnorm = mcol.Normalize(vmin=0, vmax=1)
                            m = pltcm.ScalarMappable(norm=cnorm, cmap=cm1)
                            m.set_array([0, 1])
                            cb = plt.colorbar(m, ticks=[0, 1], aspect=1000)
                            cb.set_ticklabels(["Low", "High"])
                            cb.set_label("Feature Value",
                                         size=18, labelpad=-10)
                            cb.ax.tick_params(labelsize=18, length=0)
                            cb.set_alpha(1)
                            cb.outline.set_visible(False)
                            bbox = cb.ax.get_window_extent().transformed(
                                plt.gcf().dpi_scale_trans.inverted())
                            cb.ax.set_aspect((bbox.height - 0.9) * 20)

                            plt.savefig(path+"/{}_ShapSummaryPlot_{}_{}.png".format(
                                condition, class_name, class_group),
                                bbox_inches='tight', dpi=600)
                            plt.show()
                else:
                    print("No predictions for class {}!".format(class_name))

        # get gene predictions for output
        return df_scores, ypred

    else:   # no y_true given (assume that classes are unknown)
        num_class = len(class_names)

        print(
            "# of Predicted Phos. Genes-Rxn Pairs: {}".format(Counter(ypred)[0]))
        print(
            "# of Predicted Unreg. Genes-Rxn Pairs: {}".format(Counter(ypred)[1]))
        print(
            "# of Predicted Acetyl. Genes-Rxn Pairs: {}".format(Counter(ypred)[2]))

        # create new dataset with features, gene names and predicted classes
        # reset indices
        df_new = X_test.copy()
        df_new["genes"] = gene_reactions.genes
        df_new["reaction"] = gene_reactions.reaction
        df_new["ypred"] = ypred

        acetylGenesPred = gene_reactions[ypred == 2]
        phosGenesPred = gene_reactions[ypred == 0]

        # create boxplots of features, grouped by predicted class
        numeric_feats = X_test.select_dtypes(include='float64').columns
        pltFont = {'fontname': 'Arial'}

        y_classes = np.where(ypred == 0, 'Ph',
                             np.where(ypred == 1, 'Un', 'Ac'))

        sns.set()
        f, axs = plt.subplots(3, 4, figsize=(8, 6))
        for i, ax in enumerate(axs.reshape(-1)):
            sns.boxplot(y_test=df_new[numeric_feats[i]], x=y_classes,
                        ax=ax, order=["Ph", "Un", "Ac"])
            ax.set_xlabel('')   # remove x-axis label
            ax.set_ylabel(numeric_feats[i], fontsize=16, **pltFont)
            ax.tick_params(axis='both', which='major',
                           labelsize=16)
        plt.tight_layout()
        plt.savefig(path+"/{}_predictionsBoxplot.png".format(condition),
                    bbox_inches='tight', dpi=600)
        plt.show()

        if save:
            for class_num, class_name in zip([0, 2], ["Phos", "Acetyl"]):
                DEGs = gene_reactions.iloc[ypred == class_num]
                if len(DEGs) > 0:
                    DEGs.to_csv('../results/{}_Predicted{}Genes.csv'.format(condition, class_name),
                                index=False)

        return acetylGenesPred, phosGenesPred, ypred


def plot_roc(clf, X_train, y_train, X_test, y_test,
             class_names, pos_class=None,
             figsize=(10, 6), show=True):
    '''
    This function is used to calculate AUC and plot the ROC curve
    for multi-class problems.

    Function Inputs:
    ----------
    1. clf:             Classifier model
    1. X_train:         Feature matrix used to train model
    2. y_train:         Target variable array used to train model
    1. X_test:          Feature matrix that model is making predictions on
    2. y_test:          Target variable array that model performance is measured against
    7. class_names:     String array of class names
    8. pos_class:       Positive class. If given, only the curve for this class will be
                        shown.
    9. fig_size:        Size of ROC curve plot

    Function Outputs: 
    ----------
    1. avg_auc:     Mean AUC calculated for all classes using the OneVsRest method.
    2. fig:         Figure object containing the ROC curve
    '''

    n_classes = len(class_names)

    if n_classes > 2:
        y_train = label_binarize(y_train, classes=[0, 1, 2])
        y_test = label_binarize(y_test, classes=[0, 1, 2])

        tpr = dict()
        classifier = OneVsRestClassifier(clf)
        y_score = classifier.fit(X_train, y_train).predict_proba(X_test)

        # Plotting and estimation of FPR, TPR
        pltFont = {'fontname': 'Arial'}

        fpr = dict()
        roc_auc = dict()

        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        plt.rcParams.update(plt.rcParamsDefault)
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot([0, 1], [0, 1], 'k--')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xticklabels(ax.get_xticks(), fontsize=14, **pltFont)
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        ax.set_yticklabels(ax.get_yticks(), fontsize=14, **pltFont)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        ax.set_xlabel('False Positive Rate', fontsize=16, **pltFont)
        ax.set_ylabel('True Positive Rate', fontsize=16, **pltFont)
        ax.set_title('ROC Curve', fontsize=18, **pltFont)

        if isinstance(pos_class, int):
            ax.plot(fpr[pos_class], tpr[pos_class], label='{} vs. Rest (AUC = {:.3f})'.format(
                class_names[pos_class], roc_auc[pos_class]))
        else:
            for i in range(n_classes):
                ax.plot(fpr[i], tpr[i], label='{} vs. Rest (AUC = {:.3f})'.format(
                    class_names[i], roc_auc[i]))

        ax.grid(alpha=.4)
        ax.legend(loc="lower right", fontsize=14)
        sns.despine()
        if show is True:
            plt.show()
        else:
            plt.close()

        avg_auc = np.nanmean(list(roc_auc.values()))

    else:   # binary problem
        print("ROC BINARY PROBLEM!")

        # probs = clf.predict_proba(X_test)
        # preds = probs[:,pos_class]
        # fpr, tpr, threshold = roc_curve(y_test, preds)
        # avg_auc = auc(fpr, tpr)

        # # plot
        # fig, ax = plt.subplots(figsize=figsize)

        # plt.title('ROC Curve')
        # plt.plot(fpr, tpr, 'b', label = 'AUC = %0.3f' % avg_auc)
        # plt.legend(loc = 'lower right')
        # plt.plot([0, 1], [0, 1],'r--')
        # plt.xlim([0, 1])
        # plt.ylim([0, 1])
        # plt.ylabel('True Positive Rate')
        # plt.xlabel('False Positive Rate')
        # if show is True:
        #     plt.show()
        # else:
        #     plt.close()

    return avg_auc, fig


def shap_dependence(explainer, features,
                    shap_values, interaction_values,
                    var1, var2,
                    class_names, condition,
                    figsize=(6, 10)):
    '''
    This function is used to plot SHAP dependence plots given
    SHAP values and/or interaction values. This function is not used anywhere for the
    CAROM manuscript and is not complete.

    Function Inputs:
    ----------

    Function Outputs: 
    ----------

    '''

    num_class = len(class_names)

    if shap_values:
        fig, axes = plt.subplots(
            nrows=num_class, ncols=1, figsize=figsize, sharex=False, sharey=False)
        for i in range(num_class):
            shap.dependence_plot(ind=var1,
                                 shap_values=shap_values[i],
                                 features=features,
                                 interaction_index=var2,
                                 ax=axes[i],
                                 alpha=0.5,
                                 show=False)
            axes[i].set_title(class_names[i], fontsize=14)
        fig.suptitle(condition, fontsize=18)
        plt.tight_layout()
        plt.show()

    if (interaction_values) and (var2 != "auto"):
        fig, axes = plt.subplots(
            nrows=num_class, ncols=1, figsize=figsize, sharex=False, sharey=False)
        for i in range(num_class):
            shap.dependence_plot((var1, var2),  # maxATPafterKO, rawVmin/max
                                 shap_values=interaction_values[i],
                                 features=features,
                                 interaction_index="auto",
                                 alpha=0.5,
                                 ax=axes[i],
                                 show=False)
            axes[i].set_title(class_names[i], fontsize=14)
        fig.suptitle("SHAP Interaction: {}".format(condition), fontsize=18)
        plt.tight_layout()
        plt.show()

        # fig2, axes2 = plt.subplots(nrows=num_class, ncols=1, figsize=figsize,sharex=False,sharey=False)
        # for i in range(num_class):
        #     shap.dependence_plot((var1, var1), #maxATPafterKO, rawVmin/max
        #          shap_values = interaction_values[i],
        #          features = features,
        #          alpha=0.50,
        #          ax=axes2[i],
        #          show=False)
        #     axes2[i].set(xlabel='', ylabel='')
        #     axes2[i].set_title(class_names[i],fontsize=14)
        # fig2.suptitle("SHAP Interaction: {}".format(condition), fontsize=18)
        # plt.tight_layout()
        # plt.show()
