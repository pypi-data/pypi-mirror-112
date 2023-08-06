from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.impute import SimpleImputer as Imputer
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
from scipy.stats import boxcox_normmax
from scipy import stats, special
from statsmodels.stats.outliers_influence import OLSInfluence,variance_inflation_factor
import statsmodels.api as sm
from codes.Tools import *
from sklearn.preprocessing import MinMaxScaler, Normalizer, StandardScaler,QuantileTransformer
import warnings

warnings.filterwarnings('ignore')

class ImputerAttr(BaseEstimator, TransformerMixin):

    def __init__(self, strategy, knn_param=5, base_impute=None):
        self.strategy = strategy  ## strategy = 0:普通填充，1：knn填充
        self.knn_param = knn_param  ### 可接受一个值或者一个列表 ，当接收一个列表，会进行搜索，返回最优的k对应的结果
        self.base_impute = base_impute  #### 均值，众数或者一般常数填充

    def fit(self, df_s, cols):  ### cols 是需要填补的的特征
        df = df_s.copy()
        if 'object' in df[cols].dtypes:
            msg = 'please check the type of cols '
            return {'status': 1, 'msg': msg, 'res': None}
        if self.strategy == 0:
            X = df[cols].values
            self.model = Imputer(strategy=self.base_impute) 
            self.model.fit(X)
        elif self.strategy == 1:
            knn_param = self.knn_param if type(self.knn_param) == list else [self.knn_param]
            self.model = {}
            all_cols = df.columns
            for col in all_cols[:]:
                if df[col].dtypes == 'object':
                    all_cols.remove(col)
            self.all_cols = all_cols
            for col in cols:
                if df[col].dtypes != 'object':
                    model_tmp = GridSearchCV(KNeighborsRegressor(), param_grid={'n_neighbors': knn_param})
                else:
                    model_tmp = GridSearchCV(KNeighborsClassifier(), param_grid={'n_neighbors': knn_param})
                train_idx = [j for j in range(df.shape[0]) if
                             j not in [i for i in range(df.shape[0]) if np.isnan(df.loc[i, col])]]
                train_cols = list(set(all_cols).difference(set([col])))
                X_train = Imputer(strategy='mean').fit_transform(df[train_cols])[train_idx]
                model_tmp.fit(X_train, df[col].values[train_idx])
                self.model[col] = model_tmp
        else:
            return {'status': 1, 'msg': 'Ineffective strategy', 'res': None}

        return {'status': 0, 'msg': '', 'res': None}

    def transform(self, df_s, cols) :
        df = df_s.copy()
        if self.strategy == 0:
            df[cols] = self.model.transform(df[cols].values)
            return {'status': 0, 'msg': '', 'res': df}
        else:
            for col in cols:
                model_tmp = self.model[col]
                train_cols = list(set(self.all_cols).difference(set([col])))
                x = Imputer(strategy='mean').fit_transform(df[train_cols])
                pre_idx = [i for i in range(df.shape[0]) if np.isnan(df.loc[i, col])]
                if len(pre_idx) > 0:
                    df.loc[df.index.isin(pre_idx), col] = model_tmp.predict(x[pre_idx])
            return {'status': 0, 'msg': '', 'res': df}

    def save_model(self):
        return {'status': 0, 'msg': '', 'res': self.model}


class DataTransAttr(BaseEstimator, TransformerMixin):

    def __init__(self, strategy, sc_range=(0, 1)):
        self.strategy = strategy  ### 0：Z分数标准化，1：标量化（任意尺度范围），2：偏度纠正(可不必先归一化) ,3:双峰分布
        self.sc_range = sc_range  ## 如果为空，则默认0-1，一般有0-1，-1-1 ,

    def fit(self, df_s, cols):
        df = df_s.copy()
        if self.strategy == 0:
            self.model = StandardScaler()
            self.model.fit(df[cols].values)
        elif self.strategy == 1:
            self.model = MinMaxScaler(feature_range=self.sc_range)
            self.model.fit(df[cols].values)
        elif self.strategy==3:
            self.model = QuantileTransformer(n_quantiles=100,output_distribution='normal', random_state=0)
            self.model.fit(df[cols].values)
        elif self.strategy == 2:
            self.model = {}
            for col in cols:
                S, M = df[col].min(), df[col].max()
                sk = df[col].skew()
                print(sk, S, M)
                if sk >= 0:
                    df[col] = df[col] - S + 1e-5
                    lambda_ = stats.boxcox(df[col].values)[1]
                else:  #### 左偏先转成右偏才能起作用
                    df[col] = M - df[col] + 1e-5
                    lambda_ = stats.boxcox(df[col].values)[1]

                self.model[col] = (sk, S, M, lambda_)
        else:
            return {'status': 1, 'msg': 'Ineffective strategy', 'res': None}

        return {'status': 0, 'msg': '', 'res': None}

    def transform(self, df_s, cols):
        df = df_s.copy()
        if (self.strategy == 0) or (self.strategy == 1) or (self.strategy == 3):
            df[cols] = self.model.transform(df[cols].values)
        else:
            for col in cols:
                sk, S, M, lambda_ = self.model[col]
                if sk > 0:
                    df[col] = df[col] - S + 1e-5
                    df[col] = stats.boxcox(df[col].values, lmbda=lambda_)
                else:
                    df[col] = M - df[col] + 1e-5
                    df[col] = stats.boxcox(df[col].values, lmbda=lambda_)

        return {'status': 0, 'msg': '', 'res': df}

    def save_model(self):

        return {'status': 0, 'msg': '', 'res': self.model}

    def invboxcox(self, y, tup): ###  self.strategy == 2 专用
        (sk, S, M, ld) = tup
        if ld == 0:
            inv_y = np.exp(y)
            y_s = inv_y - 1e-5 + S if sk >= 0 else M - inv_y + 1e-5
            return y_s
        else:
            inv_y = np.exp(np.log(ld * y + 1) / ld)
            y_s = inv_y - 1e-5 + S if sk >= 0 else M - inv_y + 1e-5
            return y_s


class OutlierAttr(BaseEstimator, TransformerMixin):

    def __init__(self, strategy,threshold_s):
        self.strategy = strategy  ##### 1:异常点 ，2：高杠杆点 ，3:强影响点
        self.threshold_s = threshold_s  #### 一般阈值分别为 ： 1:2，2:2  ，3:0.5

    def fit(self, df_s, cols): ### cols 为参与处理的特征，y_label 是真实存在的,只能对训练集操作
        df = df_s.reset_index(drop=True).copy()
        md= sm.OLS(df['y_label'],df[cols].values).fit()
        self.if_result = OLSInfluence(md).summary_frame()
        self.if_result['hat_v/mean'] = self.if_result['hat_diag']/self.if_result['hat_diag'].mean()
        if self.strategy not in [1,2,3]:
            return {'status': 1, 'msg': 'Ineffective strategy', 'res': None}

        return {'status': 0, 'msg': '', 'res': None}

    def transform(self, df_s, cols):
        df = df_s.reset_index(drop=True).copy()
        if self.strategy==1:
            df['judgment'] = self.if_result['student_resid']
        elif self.strategy==2:
            df['judgment'] = self.if_result['hat_v/mean']
        elif self.strategy==3:
            df['judgment'] = self.if_result['cooks_d']
        else:
            return {'status': 1, 'msg': 'Ineffective strategy', 'res': None}
        df = df[df['judgment']<self.threshold_s].reset_index(drop=True)

        return {'status': 0, 'msg': '', 'res': df}

    def save_model(self):  ##### 返回的是每条样本的统计值，只能对训练集操作,不能对测试集操作

        return {'status': 0, 'msg': '', 'res':self.if_result}


class CorrAttr(BaseEstimator, TransformerMixin):
    def __init__(self, strategy=1, threshold_s=0.8):
        self.strategy = strategy ##### 1： 相关系数法 2: 膨胀因子法
        self.threshold_s = threshold_s  ### 相关系数阈值默认0.8，膨胀因子一般设置10


    def fit(self,df_s,cols):
        df = df_s.copy()

        if self.strategy==1:
            df_corr = df[cols].corr().abs()
            corr_high = df_corr.applymap(lambda x: np.nan if x > self.threshold_s else x).isnull()
            n = len(cols)
            corr_pair = []
            for i in range(n):
                for j in range(i + 1, n):
                    if corr_high.loc[cols[i], cols[j]] == True:
                        corr_pair.append([cols[i], cols[j]])
            self.remove_cols = []
            for a, b in corr_pair:
                t = df_corr[a].mean()
                p = df_corr[b].mean()
                if t > p:
                    self.remove_cols.append(a)
                else:
                    self.remove_cols.append(b)
        elif self.strategy==2:
            self.remove_cols = vif(df[cols],self.threshold_s)

        else:
            return {'status': 1, 'msg': 'Ineffective strategy', 'res': None}

        return {'status': 0, 'msg': '', 'res':None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        df = df.loc[:,~df.columns.isin(self.remove_cols)]
        return {'status': 0, 'msg': '', 'res':df}

    def save_model(self):  ##### 返回的是删掉的列

        return {'status': 0, 'msg': '', 'res':self.remove_cols}


class SparseAttr(BaseEstimator, TransformerMixin):

    def __init__(self,strategy,threshold_s):
        self.strategy = strategy ## 1:是最常见的取值频数和第二常见的取值频数之间的比值 法 2: 样本量与 不同取值数目的比值 法
        self.threshold_s = threshold_s

    def fit(self,df_s,cols):
        df = df_s.copy()
        self.remove_cols = []
        if self.strategy==1:
            for col in cols:
                a,b = list(df.groupby([col])['y_label'].count().reset_index().sort_values(by='y_label', ascending=False)[
                         'y_label'])[:2]
                t = a/b
                print(t,col)
                if t>self.threshold_s:
                    self.remove_cols.append(col)

        elif self.strategy==2:
            for col in cols:
                a,b = df[col].nunique() ,df.shape[0]
                t = b/a
                if t>self.threshold_s:
                    self.remove_cols.append(col)
        else:
            return {'status': 1, 'msg': 'Ineffective strategy', 'res': None}

        return {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        df = df.loc[:,~df.columns.isin(self.remove_cols)]
        return {'status': 0, 'msg': '', 'res':df}

    def save_model(self):  ##### 返回的是删掉的列

        return {'status': 0, 'msg': '', 'res':self.remove_cols}

class TSproAttr(BaseEstimator, TransformerMixin):  #### 假设是标准格式 ，则必有至少两个arr 字段 ： ts(时间戳),和至少一个参数arr

    def __init__(self,strategy,param):
        self.strategy = strategy  ####### 1:指定频率采样 ，2：指定窗口移动平均 ，3：
        self.param = param


    def fit(self,df_s,cols):
        df = df_s.copy()

        if self.strategy==1:
            chunks = []
            for sampleid in df['sample_id'].unique():
                tmp_dict = {}
                tmp = df.loc[df['sample_id'] == sampleid, ['sample_id', 'ts'] + cols]
                y = df.loc[df.sample_id == sampleid, 'y_label']
                for col in ['ts'] + cols:
                    tmp_dict[col] = to_lst(tmp[col].values[0])

                tmp_df = pd.DataFrame(tmp_dict)
                tmp_df['ts'] = tmp_df['ts'].apply(lambda x: pd.to_datetime(x * 1000, unit='ms'))
                tmp_df = tmp_df.sort_values(by='ts').set_index('ts')
                tmp_df = tmp_df[~tmp_df.index.duplicated()]

                ks = ['linear', 'time', 'index', 'values', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic',
                      'barycentric', 'krogh', 'from_derivatives', 'piecewise_polynomial', 'pchip', 'akima', 'cubicspline']
                resample_dict = {}
                for col in cols:
                    a = tmp_df[col].values
                    bst_b = tmp_df[col].resample(self.param).interpolate('linear')
                    bst_s = 1000
                    for mtd in ks:
                        try:
                            b = tmp_df[col].resample(self.param).interpolate(mtd).bfill().ffill().fillna(0).values
                            s = sim(a, b)
                            if s < bst_s:
                                bst_s = s
                                bst_b = b
                        except:
                            pass
                    resample_dict[col] = bst_b

                resample_df = pd.DataFrame(resample_dict,
                                           index=tmp_df[col].resample(self.param).interpolate('linear').index).reset_index()
                resample_df['sample_id'] = sampleid
                extr_tmp = resample_df.groupby('sample_id').agg(lambda x: list(x)).reset_index()
                extr_tmp['y_label'] = y
                chunks.append(extr_tmp)
                print(sampleid, ' ~ down')

            self.extr_df = pd.concat(chunks)
        elif self.strategy==2:
            chunks = []
            for sampleid in df['sample_id'].unique():
                tmp_dict = {}
                tmp = df.loc[df['sample_id'] == sampleid, ['sample_id', 'ts'] + cols]
                y = df.loc[df.sample_id == sampleid, 'y_label']
                for col in ['ts'] + cols:
                    tmp_dict[col] = to_lst(tmp[col].values[0])

                tmp_df = pd.DataFrame(tmp_dict)
                tmp_df['ts'] = tmp_df['ts'].apply(lambda x: pd.to_datetime(x * 1000, unit='ms'))
                tmp_df = tmp_df.sort_values(by='ts').set_index('ts')

                tmp_df[cols] = tmp_df[cols].rolling(window=self.param).mean()
                tmp_df['sample_id'] = sampleid
                tmp_df = tmp_df.dropna()
                tmp_df = tmp_df.groupby('sample_id').agg(lambda x: list(x)).reset_index()
                tmp_df['y_label'] = y
                chunks.append(tmp_df)
                print(sampleid,'~ down')

            self.extr_df = pd.concat(chunks)

        else :
            return {'status': 1, 'msg': 'Ineffective strategy', 'res': None}

        return {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):

        return {'status': 0, 'msg': '', 'res': self.extr_df}



class CtgAttr(BaseEstimator, TransformerMixin):  ####

    def __init__(self,strategy,dict_cols={}):
        self.strategy = strategy   ## 仅字典编码和label编码, 字典编码则需要提供映射关系
        self.dict_cols = dict_cols

    def fit(self,df_s,cols):
        df = df_s.copy()
        if self.strategy==1:
            for col in cols:
                if col in self.dict_cols.keys():
                    #dict_tmp = self.dict_cols[col]
                    #df[col] = df[col].apply(lambda x: dict_tmp[x])
                    pass
                else:
                    dict_tmp = dict([(j, i) for i, j in enumerate(df[col].unique())])
                    self.dict_cols[col] = dict_tmp
        else:
            return  {'status': 1, 'msg': 'Ineffective strategy', 'res': None}

        return  {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        for col in cols:
            if col in self.dict_cols.keys():
                df[col+'_code'] = df[col].apply(lambda x: self.dict_cols[col][x] if x in self.dict_cols[col].keys() else -1  )
            else:
                pass
        return  {'status': 0, 'msg': '', 'res': df}

    def save_model(self):  ##### 返回的是编码列表

        return {'status': 0, 'msg': '', 'res':self.dict_cols}

