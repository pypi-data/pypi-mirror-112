import os
import pandas as pd
import numpy as np
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import KFold, RepeatedKFold
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import warnings
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import kurtosis
import inspect, re
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings

warnings.filterwarnings('ignore')


class TwoNomal():
    ###生成双峰分布
    def __init__(self, mu1, mu2, sigma1, sigma2):
        self.mu1 = mu1
        self.sigma1 = sigma1
        self.mu2 = mu2
        self.sigma2 = sigma2

    def doubledensity(self, x):
        mu1 = self.mu1
        sigma1 = self.sigma1
        mu2 = self.mu2
        sigma2 = self.sigma1
        N1 = np.sqrt(2 * np.pi * np.power(sigma1, 2))
        fac1 = np.power(x - mu1, 2) / np.power(sigma1, 2)
        density1 = np.exp(-fac1 / 2) / N1

        N2 = np.sqrt(2 * np.pi * np.power(sigma2, 2))
        fac2 = np.power(x - mu2, 2) / np.power(sigma2, 2)
        density2 = np.exp(-fac2 / 2) / N2
        # print(density1,density2)
        density = 0.5 * density2 + 0.5 * density1
        return density


def vif(X, thres=10.0):
    col = list(range(X.shape[1]))
    dropped = True
    remove_cols = []
    while dropped:
        dropped = False
        vif = [variance_inflation_factor(X.iloc[:, col].values, ix)
               for ix in range(X.iloc[:, col].shape[1])]
        maxvif = max(vif)
        maxix = vif.index(maxvif)
        if maxvif > thres:
            print('delete=', X.columns[col[maxix]], '  ', 'vif=', maxvif)
            remove_cols.append(X.columns[col[maxix]])
            del col[maxix]
            dropped = True
    print('Remain Variables:', list(X.columns[col]))
    print('VIF:', vif)
    return remove_cols


###########基于形态计算相似度
def sim(s1, s2):
    s1 = [i for i in s1 if not np.isnan(i)]
    s2 = [i for i in s2 if not np.isnan(i)]
    a1, b1, c1, d1 = max(s1), min(s1), np.std(s1), np.mean(s1)
    a2, b2, c2, d2 = max(s2), min(s2), np.std(s2), np.mean(s2)
    dis = abs(a1 - a2) / max(abs(a1), abs(a2), 1e-10) + abs(b1 - b2) / max(abs(b1), abs(b2), 1e-10) + abs(
        c1 - c2) / max(abs(c1), abs(c2), 1e-10) + abs(d1 - d2) / max(abs(d1), abs(d2), 1e-10)

    return dis


def to_lst(s):
    if type(s) == str:
        r = [float(i) for i in s[1:-1].split(',')]
    else:
        pass
    return list(r)


def model_RF(train_df, test_df, train_cols, param_rf, ty):
    X_data = np.array(train_df[train_cols].values)
    Y_data = np.array(train_df['AVG_REMOVAL_RATE'].values)
    X_test = np.array(test_df[train_cols].values)
    Y_test = np.array(test_df['AVG_REMOVAL_RATE'].values)

    folds = KFold(n_splits=15, shuffle=True, random_state=2021)
    oof_rf = np.zeros(len(X_data))
    predictions_t_rf = np.zeros(len(X_test))
    predictions_train_rf = np.zeros(len(X_data))
    feature_importance_df_rf = pd.DataFrame()
    model = RandomForestRegressor(oob_score=True, random_state=10, verbose=0, criterion='mse', **param_rf)
    for fold_, (train_idx, valid_idx) in enumerate(folds.split(X_data, Y_data)):
        print(fold_, '~')
        model.fit(X_data[train_idx], Y_data[train_idx])

        fold_importance_df = pd.DataFrame({'feature': train_cols, 'importance': model.feature_importances_})
        fold_importance_df["fold"] = fold_ + 1
        feature_importance_df_rf = pd.concat([feature_importance_df_rf, fold_importance_df], axis=0)

        oof_rf[valid_idx] = model.predict(X_data[valid_idx])
        predictions_t_rf += model.predict(X_test) / folds.n_splits
        predictions_train_rf += model.predict(X_data) / folds.n_splits

        print(mean_squared_error(model.predict(X_test), Y_test))

    mtr = [mean_squared_error(Y_test, predictions_t_rf), r2_score(Y_test, predictions_t_rf),
           mean_absolute_error(Y_test, predictions_t_rf)]
    print(mean_squared_error(Y_data, predictions_train_rf))
    print(mean_squared_error(Y_data, oof_rf))
    print(mtr)

    rf_imp = feature_importance_df_rf.groupby(['feature'])['importance'].mean().sort_values().reset_index()
    rf_imp['md'] = 'rf'
    rf_imp['importance'] = rf_imp['importance'].apply(lambda x: x / (np.sum(rf_imp['importance'])))
    rf_imp['type'] = ty

    return rf_imp, oof_rf, predictions_t_rf, mtr


def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)

    percentile_.__name__ = 'percentile%s' % n
    return percentile_


def kurt():
    def kurt_(x):
        return kurtosis(x)

    kurt_.__name__ = 'kurt'
    return kurt_


sta_methods = ['min', 'max', 'median', 'skew', 'mean', 'std', kurt(), percentile(10), percentile(25), percentile(75),
               percentile(90)]


def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
        return m.group(1)


isfunc = type(kurt())
