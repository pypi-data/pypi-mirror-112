import argparse

from carom import split_train_test, carom


def main():
    # region
    parser = argparse.ArgumentParser(prog='carom',
                                     description='CAROM is the machine learning tool described in the article Metabolic signatures of regulation by phosphorylation and acetylation by Chandrasekaran, Lee, Shen and Smith.')

    parser.add_argument("-f", nargs='?', metavar='filename',
                        help='set which file to be handle. Default is "https://github.com/KardelUM/Carom/raw/master/caromDataset.csv"',
                        default=None)
    # parser.add_argument("--no-shapley", default=False, action="store_true", help="don't compute shapley")
    parser.add_argument("--no-prediction", default=False, action="store_true", help="don't do prediction")
    parser.add_argument("--no-genetic-selection", default=False, action="store_true", help="don't do genetic selection")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.2')
    parser.print_help()
    args = parser.parse_args()
    print(args.f)
    print("args.filename:", args.f)
    print("args.no_pred:", args.no_prediction)
    print("args.no_gselection:", args.no_genetic_selection)
    # endregion
    filename = args.f
    no_p = args.no_prediction
    no_g = args.no_genetic_selection

    df_train, df_test = split_train_test(filename)
    feature_names = df_train.columns[3:16]

    ### train model ###
    [xgb_model, scores] = carom.train_model(
        X=df_train[feature_names],
        y=df_train['Target'],
        num_iter=5,
        condition="TestInstall",
        fig_path="./figures/training")

    ### Shapley analysis ###
    [shap_explainer, shap_values] = carom.shapley(
            xgbModel=xgb_model,
            X=df_train[feature_names],
            condition="TestInstall",
            fig_path="./figures/shap")

    ### make new predictions ###
    if no_p:
        [scores, y_pred] = carom.make_predictions(
            mdl=xgb_model,
            X_test=df_test[feature_names], y_test=df_test["Target"],
            X_train=df_train[feature_names], y_train=df_train["Target"],
            class_names=["Phos", "Unreg", "Acetyl"],
            gene_reactions=df_test[['genes', 'reaction']],
            explainer=shap_explainer,
            condition="TestInstall",
            fig_path="./figures/validation")

    ### analyze select genes ###

    # get first Phos gene and first Acetyl gene
    phos_gene = df_test.genes[df_test.Target == -1].iloc[0]
    acetyl_gene = df_test.genes[df_test.Target == 1].iloc[0]

    select_genes = [phos_gene, acetyl_gene]
    print(select_genes)
    if not no_g:
        carom.select_genes(X=df_test[feature_names], y=df_test["Target"],
                           all_genes=df_test[['genes', 'reaction']],
                           select_genes=select_genes,
                           condition="TestInstall",
                           class_names=["Phos", "Unreg", "Acetyl"],
                           model=xgb_model,
                           explainer=shap_explainer,
                           fig_path="./figures/select_genes")

