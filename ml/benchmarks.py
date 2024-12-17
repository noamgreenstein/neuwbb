from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold


def generate(data):
    data_dict = {}
    df1, df2 = data
    df1.fillna(0, inplace=True)
    df2.fillna(0, inplace=True)
    n1, n2 = df1.shape[0], df2.shape[0]

    y = np.concatenate([np.ones(n1), np.zeros(n2)])

    for column in df1.columns:
        total_stat = np.concatenate([df1[column].values, df2[column].values])

        kfold = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)

        x = np.array(total_stat).reshape(-1, 1)
        auc_scores = []
        optimal_thresholds = []
        directions = []
        optimal_nums = []

        # Cross-validation loop
        for train_index, test_index in kfold.split(x, y):
            x_train, x_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]

            logr = LogisticRegression()
            logr.fit(x_train, y_train)

            y_prob = logr.predict_proba(x_test)[:, 1]
            fpr, tpr, thresholds = roc_curve(y_test, y_prob)
            auc_scores.append(auc(fpr, tpr))

            optimal_idx = np.argmax(tpr - fpr)
            optimal_threshold = thresholds[optimal_idx]
            optimal_thresholds.append(optimal_threshold)

            beta_0 = logr.intercept_[0]
            beta_1 = logr.coef_[0][0]
            direction = 'Normal' if beta_1 > 0 else 'Reverse' if beta_1 < 0 else 'Flat'
            directions.append(direction)

            optimal_nums.append((np.log(
                optimal_threshold / (1 - optimal_threshold)) - beta_0) / beta_1)

        average_auc = np.mean(auc_scores)
        most_common_direction = max(set(directions), key=directions.count)
        optimal_stat = np.mean(optimal_nums)

        data_dict[column] = {
            'AUC': average_auc,
            'optimal amount': optimal_stat,
            'direction': most_common_direction
        }

    return data_dict
