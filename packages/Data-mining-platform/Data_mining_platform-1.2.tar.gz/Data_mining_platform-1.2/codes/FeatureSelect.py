from sklearn.model_selection import GridSearchCV,cross_val_score, ShuffleSplit
from sklearn.ensemble import RandomForestRegressor ,RandomForestClassifier
import numpy as np
import pandas as pd
from codes.Tools import *
from scipy.stats import pearsonr
from minepy import MINE
import dcor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as Lda
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold,SelectKBest,chi2,SelectFromModel,RFE
import warnings

warnings.filterwarnings('ignore')


class Filter():

    def __init__(self,strategy,threshold_s,bestk):
        self.strategy = strategy  #### 1:移除低方差 ，2：卡方检验 , 3:Pearson相关系数 ,4:最大信息系数 ,5:距离相关系数 ,6:基于模型,回归 ，7：基于模型 分类
        self.threshold_s = threshold_s
        self.bestk = bestk

    def fit(self,df_s,cols):
        df = df_s
        if self.strategy == 1:
            vc = VarianceThreshold(threshold=self.threshold_s)
            vc.fit(df[cols])
            n = len(cols)

            self.delete_lst = []
            for i in range(n):
                if not vc.get_support()[i]:
                    if dcor.distance_correlation(df[cols[i]], df['y_label']) <0.05:
                        self.delete_lst.append(cols[i])

        elif self.strategy == 2:
            cc = SelectKBest(chi2,self.bestk)
            cc.fit(df[cols],df['y_label'])
            n = len(cols)

            self.delete_lst = []
            for i in range(n):
                if not cc.get_support()[i]:
                    self.delete_lst.append(cols[i])


        elif self.strategy == 3:
            self.delete_lst = []
            for col in cols :
                if pearsonr(df[col],df['y_label'])[1].abs()<self.threshold_s:
                    self.delete_lst.append(col)

        elif self.strategy == 4:
            self.delete_lst = []
            m = MINE()
            for col in cols :
                if m.compute_score(df[col],df['y_label']).mic() <self.threshold_s:
                    self.delete_lst.append(col)

        elif self.strategy == 5:
            self.delete_lst = []
            for col in cols :
                if dcor.distance_correlation(df[col],df['y_label']).mic() <self.threshold_s:
                    self.delete_lst.append(col)

        elif self.strategy == 6:  ##### 回归
            self.delete_lst = []
            for col in cols :
                rf = RandomForestRegressor(n_estimators=20, max_depth=4)
                for col in cols:
                    score = cross_val_score(rf, df[col], df['y_label'], scoring="r2", cv=ShuffleSplit(df.shape[0], 3, .3))
                    if score <self.threshold_s:
                        self.delete_lst.append(col)

        elif self.strategy == 7:  ##### 分类
            self.delete_lst = []
            for col in cols :
                rf = RandomForestClassifier(n_estimators=20, max_depth=4)
                for col in cols:
                    score = cross_val_score(rf, df[col], df['y_label'], scoring="auc", cv=ShuffleSplit(df.shape[0], 3, .3))
                    if score <self.threshold_s:
                        self.delete_lst.append(col)
        else:
            return {'status': 1, 'msg': 'Ineffective strategy', 'res': None}

        return  {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        df = df.loc[:,~df.columns.isin(self.delete_lst)]

        return {'status': 0, 'msg': '', 'res': df}

    def sava_model(self):

        return  {'status': 0, 'msg': '', 'res': self.delete_lst}


class Wrapper(): ############### 特征递归消除

    def __init__(self,strategy,bestk):
        self.strategy = strategy  ### 1：回归，2：分类
        self.bestk = bestk

    def fit(self,df_s,cols):
        df = df_s.copy()
        if self.strategy == 1:
            rfe = RFE(estimator=RandomForestRegressor(n_estimators=100,max_depth='sqrt'), n_features_to_select=self.bestk)
        elif self.strategy == 2:
            rfe = RFE(estimator=RandomForestClassifier(n_estimators=100, max_depth='sqrt'),n_features_to_select=self.bestk)

        rfe.fit(df[cols],df['y_label'])
        n = len(cols)

        self.delete_lst = []
        for i in range(n):
            if not rfe.get_support()[i]:
                self.delete_lst.append(cols[i])


        return  {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        df = df.loc[:,~df.columns.isin(self.delete_lst)]

        return {'status': 0, 'msg': '', 'res': df}


    def save_model(self):

        return {'status': 0, 'msg': '', 'res': self.delete_lst}

class Embedded():

    def __init__(self,strategy,base_model,threshold_s ):  ## 来选择不为0的系数
        #self.strategy = strategy ### 1：L1 ，2：稀疏矩阵 ，3：基于树
        self.base_model = base_model   ## 1:{ 1:svc ,2:lasso,3:lr }
        #self.threshold_s = threshold_s

    def fit(self,df_s,cols):
        df = df_s.copy()
        if self.strategy == 1:
            ##lsvc = LinearSVC(C=0.01, penalty="l1", dual=False)
            ## GradientBoostingClassifier()
            ### LogisticRegression(penalty="l1", C=0.1)
            self.base_model.fit(df[cols].values, df['y_label'])
            sfm = SelectFromModel(self.base_model, prefit=True)
            n = len(cols)

            self.delete_lst = []
            for i in range(n):
                if not sfm.get_support()[i]:
                    self.delete_lst.append(cols[i])

        return   {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        df = df.loc[:,~df.columns.isin(self.delete_lst)]

        return {'status': 0, 'msg': '', 'res': df}

    def save_model(self):

        return {'status': 0, 'msg': '', 'res': self.delete_lst}


class  DimensionalityReduction():

    def __init__(self,strategy,components):
        self.strategy = strategy ###1:pca, 2:lda
        self.components = components

    def fit(self,df_s,cols):
        df = df_s.copy()
        if self.strategy == 1:
            self.dr = PCA(n_components=self.components)
            self.dr.fit(df[cols])

        elif self.strategy == 2:
            self.dr = Lda(n_components=self.components)
            self.dr.fit(df[cols], df['y_label'])

        return  {'status': 0, 'msg': '', 'res': None}

    def transform(self,df_s,cols):
        df = df_s.copy()
        X =  self.dr.transform(df[cols])
        y = df['y_label']

        res ={'X':X,'y':y}
        return  {'status': 0, 'msg': '', 'res': res}

    def save_model(self):

        return  {'status': 0, 'msg': '', 'res': self.dr}

