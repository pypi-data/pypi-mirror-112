# -*- coding: utf-8 -*-
"""
Script for testing CAROM functions

Created on Mon Jun  7 13:41:25 2021
@author: kirksmi
"""

import pandas as pd
import carom

### load datasets ###

# sample training dataset (1000 random/stratified observations)
df_carom = pd.read_csv("caromDataset.csv")

# make training (~500 samples) and test (~100 samples) datasets 
# df_train = df_carom.groupby("Target").sample(n=167, random_state=1).reset_index(drop=True)
# df_test = df_carom.groupby("Target").sample(n=33, random_state=2).reset_index(drop=True)

df_train = df_carom.groupby("Target").sample(n=167, random_state=1)
df_test = df_carom.drop(df_train.index.to_list()).groupby("Target").sample(n=33, random_state=2).reset_index(drop=True)
df_train.reset_index(drop=True)



feature_names = df_train.columns[3:16]
print(feature_names)

#%%

### train model ###
[xgb_model, scores] = carom.train_model(
       	X = df_train[feature_names],
        y = df_train['Target'],
        num_iter=5,
        condition = "TestInstall",
        fig_path = "./figures/training")


### Shapley analysis ###
[shap_explainer, shap_values] = carom.shapley(
    xgbModel = xgb_model,
    X = df_train[feature_names],
    condition = "TestInstall",
    fig_path = "./figures/shap")


### make new predictions ###
[scores, y_pred] = carom.make_predictions(
                          mdl= xgb_model,
                          X_test = df_test[feature_names], y_test = df_test["Target"],
                          X_train = df_train[feature_names], y_train = df_train["Target"],
                          class_names = ["Phos", "Unreg", "Acetyl"],
                          gene_reactions = df_test[['genes', 'reaction']],
                          explainer = shap_explainer,
                          condition = "TestInstall",
                          fig_path = "./figures/validation")


### analyze select genes ###

# get first Phos gene and first Acetyl gene
phos_gene = df_test.genes[df_test.Target==-1].iloc[0]
acetyl_gene = df_test.genes[df_test.Target==1].iloc[0]


select_genes = [phos_gene, acetyl_gene] 
print(select_genes)

carom.select_genes(X = df_test[feature_names], y = df_test["Target"],
              all_genes = df_test[['genes','reaction']],
              select_genes = select_genes,
              condition = "TestInstall",
              class_names = ["Phos", "Unreg", "Acetyl"],
              model = xgb_model,
              explainer = shap_explainer,
              fig_path = "./figures/select_genes")

