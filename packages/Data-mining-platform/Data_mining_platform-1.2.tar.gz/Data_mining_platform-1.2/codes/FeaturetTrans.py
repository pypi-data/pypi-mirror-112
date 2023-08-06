from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
from scipy.stats import boxcox_normmax
from scipy import stats, special
import statsmodels.api as sm
from codes.Tools import *
from sklearn.preprocessing import MinMaxScaler, Normalizer, StandardScaler,QuantileTransformer,OneHotEncoder,LabelEncoder
import category_encoders as ce
from codes.binning import *
import warnings

warnings.filterwarnings('ignore')

class OneHot(BaseEstimator, TransformerMixin):  #### 假设已经进行了pre中的ctg转换

    def __init__(self,strategy):
        self.strategy = strategy  ### 1:保留原字段 0:删除原字段

    def fit(self,df_s,cols):
        df = df_s.copy()
        self.oh = OneHotEncoder(handle_unknown='ignore')
        self.oh.fit(df[cols].values)

        return  {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        fes = self.oh.get_feature_names()
        df[fes] = self.oh.transform(df[cols].values).toarray()
        if not  self.strategy:
            for col in cols:
                del df[col]
        return  {'status': 0, 'msg': '', 'res': df}

    def save_model(self):

        return {'status': 0, 'msg': '', 'res': self.oh}

class FreqEncoder():  ####


    def fit(self,df_s,cols):
        df = df_s.copy()
        self.ced = ce.CountEncoder()
        self.ced.fit(df[cols])

        return  {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        count_encoded = self.ced.transform(df[cols])
        df =df.join(count_encoded.add_suffix("_count"))
        return  {'status': 0, 'msg': '', 'res': df}

    def save_model(self):

        return {'status': 0, 'msg': '', 'res': self.ced}


class TarEncoder():  #### target  encoder

    def __init__(self,strategy=None):
        self.strategy = strategy

    def fit(self,df_s,cols):
        df = df_s.copy()
        self.ced = ce.TargetEncoder()
        self.ced.fit(df[cols],df['y_label'])

        return  {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        target_encoded = self.ced.transform(df[cols])
        df =df.join(target_encoded.add_suffix("_tarencode"))
        return  {'status': 0, 'msg': '', 'res': df}

    def save_model(self):

        return {'status': 0, 'msg': '', 'res': self.ced}


class BukEncoder():  #### 数据分桶

    def __init__(self,strategy,bknum=5,dis_type=1,param=None):
        self.strategy = strategy  ### 1：等距分桶，2：等频分桶 ，3：模型分桶 ，4：卡方分桶 ，5：基于业务指定划分
        self.bknum = bknum  #####指定分组个数
        self.dis_type = dis_type  #### 1:普通 ，2：对数(以10为底)
        self.param = param  ########### 指定分组划分的字典

    def fit(self,df_s,cols):
        df = df_s.copy()
        if self.strategy == 1 :
            self.d = {}
            for col in cols:
                if self.dis_type ==1:
                    print(df[col].max(),df[col].min())
                    tmp_d = (df[col].max()-df[col].min())/int(self.bknum )
                else:
                    tmp_d = (np.log10(df[col]).max()-np.log10(df[col]).min())/int(self.bknum )
                self.d[col] = tmp_d
        elif self.strategy==2:  #### 等频分桶
            self.d = {}
            for col in cols:
                self.d[col] = dict([(j,i) for i ,j in  enumerate(pd.qcut(df[col],self.bknum).unique())])

        elif self.strategy==3:  #### 决策树分箱
            self.d = {}
            for col in cols:
                boundary, sentence = optimal_binning_boundary(df[col],df['y_label'])
                self.d[col] = sentence

        elif self.strategy==4:  ### 卡方分桶
            self.d ={}
            tags = list(np.sort(df['y_label'].unique()))
            for col in cols :
                tmp_df = df[[col,'y_label']]
                result, sentence = ChiMerge3(tmp_df, 100, tags, pvalue_edge=0.01)
                self.d[col] = sentence

        elif self.strategy==5:  #### best-ks分箱
            self.d = {}
            for col in cols:
                boundary, sentence = best_ks_box(df, col, self.bknum)
                self.d[col] = sentence

        return  {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        if self.strategy == 1 :
            for col in cols:
                if self.dis_type==1:
                    df[col+'_buk1'] = np.floor_divide(df[col],self.d[col])
                else:
                    df[col + '_buk1'] = np.floor_divide(np.log10(df[col]), self.d[col])
        elif self.strategy==2:
            for col in cols:
                df[col+'_buk2'] =  df[col].apply(lambda x :  [self.d[col][k] if x in k else -1  for k in self.d[col].keys()][np.argmax([self.d[col][k] if x in k else -1  for k in self.d[col].keys() ])] )

        elif self.strategy in (3,4,5):
            for col in cols:
                df[col+'_buk'+str(self.strategy)] = df[col].apply(lambda x :eval(self.d[col]) )
        return  {'status': 0, 'msg': '', 'res': df}

    def save_model(self):
        self.rst = {'strategy':self.strategy,'bknum':self.bknum,'dis_type':self.dis_type,'model':self.d}
        return {'status': 0, 'msg': '', 'res': self.rst}


class CrossFeatures():

    def __init__(self,strategy,param=sta_methods):
        self.strategy = strategy ### 1:基于A+B  2： 基于 B+A/B(包含全部1)
        self.param = param ## 1时传统计函数列表 默认时tools里面的11个

    def fit(self,df_s,colsA,colsB):
        df = df_s.copy()
        if self.strategy in (1,2) :
            self.rst ={}
            for cola in colsA:
                tmp_df = df[[cola]].drop_duplicates().reset_index(drop=True)
                for sta in self.param:
                    tmp = df.groupby([cola])[colsB].agg(sta).reset_index()
                    tmp.columns = [cola] + [cola + '_' + c + '_' + (sta.__name__ if type(sta) == isfunc else str(sta)) for c in colsB ]
                    for colc in tmp.columns[:]:
                        if tmp[colc].nunique() ==1:
                            del tmp[colc]
                    tmp_df = pd.merge(tmp_df,tmp,on=cola,how='inner')

                self.rst[cola] = tmp_df
        return  {'status': 0, 'msg': '', 'res': None}


    def transform(self,df_s,colsA,colsB):
        df = df_s.copy()
        if self.strategy in (1,2) :
            for cola in colsA:
                tmp_df = self.rst[cola]
                df = pd.merge(tmp_df,df,on=cola,how='inner')
            if self.strategy == 2:
                for colb in colsB:
                    for cola in colsA:
                        try:
                            df[cola+'_minus_'+cola+'_'+colb+'_mean_sc'] = (df[colb] - df[cola+'_'+colb+'_mean'])/df[cola+'_'+colb+'_std']
                        except:
                            pass
                        try:
                            df[cola + '_minus_' + cola + '_' + colb + '_mean'] = df[colb] - df[cola + '_' + colb + '_mean']
                        except:
                            pass
                        try:
                            df[cola+'_'+colb+'_mgc1'] = df[cola+'_'+colb+'_median'] - df[cola+'_'+colb+'_mean']
                        except:
                            pass
                        try:
                            df[cola+'_'+colb+'_mgc2'] = df[cola+'_'+colb+'_mgc1'].abs()
                        except:
                            pass
                        try:
                            df[cola + '_' + colb + '_mgc3'] = df[cola+'_'+colb+'_median'] / (df[cola+'_'+colb+'_mean'] + 1e-5)
                        except:
                            pass
                        try:
                            df[cola + '_' + colb + '_cv'] = df[cola+'_'+colb+'_std'] / (df[cola+'_'+colb+'_mean']+ 1e-5)
                        except:
                            pass
                        try:
                            df[cola+'_'+colb+'_gap1'] = df[cola+'_'+colb+'_percentile90'] - df[cola+'_'+colb+'_percentile10']
                        except:
                            pass
                        try:
                            df[cola+'_'+colb+'_gap2'] = df[cola+'_'+colb+'_percentile80'] - df[cola+'_'+colb+'_percentile20']
                        except:
                            pass
                        try:
                            df[cola+'_'+colb+'_gap3'] = df[cola+'_'+colb+'_percentile70'] - df[cola+'_'+colb+'_percentile30']
                        except:
                            pass
                        for sta in self.param:
                            try:
                                df[colb + '_div_' + cola + '_' + colb + '_' + (sta.__name__ if type(sta) == isfunc else str(sta))] = df[colb] / (df[cola + '_' + colb + '_' + (sta.__name__ if type(sta) == isfunc else str(sta))] + 1e-5)
                            except:
                                pass
        return  {'status': 0, 'msg': '', 'res': df}

    def save_model(self):

        self.rsts = {'strategy': self.strategy,  'param': self.param, 'model': self.rst}
        return {'status': 0, 'msg': '', 'res': self.rsts}



