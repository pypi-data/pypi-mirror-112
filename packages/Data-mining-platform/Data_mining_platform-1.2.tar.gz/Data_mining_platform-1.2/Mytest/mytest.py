from codes.PreproData import *
from codes.FeaturetTrans import *
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error,r2_score
import seaborn as sns
from statsmodels.stats.outliers_influence import OLSInfluence,variance_inflation_factor
import statsmodels.api as sm
from sklearn.datasets import load_iris
from sklearn import datasets
import datetime,time,math
from scipy import interpolate
import pandas as pd
import tsfresh as tsf
from codes.Tools import *
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
import category_encoders as ce
from scipy.stats import pearsonr
from minepy import MINE
import dcor
from sklearn.svm import LinearSVC
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import VarianceThreshold,SelectKBest,chi2
from sklearn.preprocessing import MinMaxScaler, Normalizer, StandardScaler,QuantileTransformer,OneHotEncoder,LabelEncoder

pd.set_option('expand_frame_repr',False)

########################################################### 填补模块 #####################################################################
################# 生成测试数据
x0 = [ random.randint(2,200) for i in range(2000)]
x2 = [ 1/i+i**2 +random.random()*random.randint(-10,10) for i in x0]
x3 = [np.sqrt(i)+np.power(i,4)+i**2+random.random()*random.randint(-10,10) for i in x0]
#### 随机缺失
x1 = [ i if random.randint(1,40)!=5 else None for i in x0  ]

df = pd.DataFrame(data={'x1':x1,'x2':x2,'x3':x3},columns=['x1','x2','x3'])
df.isnull().sum()

############使用##################
#####均值填补
Imp = ImputerAttr(strategy=0,base_impute='mean')
Imp.fit(df,df.columns)
df_mean = Imp.transform(df,df.columns)['res']

####中位数填补
Imp1 = ImputerAttr(strategy=0,base_impute='median')
Imp1.fit(df,df.columns)
df_median = Imp1.transform(df,df.columns)['res']

######svr模型填补
Imp2 = ImputerAttr(strategy=1,knn_param=[2,4,6,8,10])
Imp2.fit(df,['x1','x2'])
df_knn = Imp2.transform(df,['x1','x2'])['res']

################################# 检查效果###################################
df_knn['x0'] = x0
df_mean['x0'] = x0
df_median['x0'] = x0

print(mean_squared_error(df_knn['x0'],df_knn['x1']))
print(mean_squared_error(df_median['x0'],df_median['x1']))
print(mean_squared_error(df_mean['x0'],df_mean['x1']))

print(r2_score(df_knn['x0'],df_knn['x1']))
print(r2_score(df_median['x0'],df_median['x1']))
print(r2_score(df_mean['x0'],df_mean['x1']))

plt.scatter(df_knn['x0'],df_knn['x1'])
plt.show()

plt.scatter(df_mean['x0'],df_mean['x1'])
plt.show()

########################################################### 数据转换模块 #####################################################################
###########################生成数据
state = np.random.RandomState(20)
x1 = state.exponential(size = 1000)  ########指数分布数据集
N2 = TwoNomal(10,80,10,10)
X2_pre = np.arange(-25,25,0.05)
x2 = N2.doubledensity(X2_pre)  ########生成双峰分布
x3 = [ np.sqrt(random.randint(2,200)) for i in range(1000)] #######随便生成一个左偏数据
len(x2)
df = pd.DataFrame(data={'x1':x1,'x2':x2,'x3':x3},columns=['x1','x2','x3'])

####### 观察原始数据
sns.distplot(x1)
plt.show()

sns.distplot(x2)
plt.show()

sns.distplot(x3)
plt.show()

########################## 先标量化
trans1 = DataTransAttr(strategy=1,sc_range=(0,1))
trans1.fit(df,df.columns)
df_sc = trans1.transform(df,df.columns)['res']

####### 观察标量化后的数据
sns.distplot(df_sc['x1'])
plt.show()

sns.distplot(df_sc['x2'])
plt.show()

sns.distplot(df_sc['x3'])
plt.show()

########################### 再 纠正分布

trans2 = DataTransAttr(strategy=2)
trans2.fit(df_sc,df_sc.columns)
df_bias = trans2.transform(df_sc,df_sc.columns)['res']
md = trans2.save_model()['res']
trans2.invboxcox(df_bias['x1'],md['x1']) -df_sc['x1']  #### 检查 逆变化，几乎相等

####### 观察纠正分布后的数据
sns.distplot(df_bias['x1'])
plt.show()

sns.distplot(df_bias['x2'])
plt.show()

sns.distplot(df_bias['x3'])  ##
plt.show()

######  strategy=3

trans3 = DataTransAttr(strategy=3)
trans3.fit(df_sc,['x2','x3'])
df_bias2 = trans3.transform(df_sc,['x2','x3'])['res']
md2 = trans3.save_model()['res']
[i[0] for i in  md2.inverse_transform(df_bias2[['x2','x3']]) ] - df_sc['x2'] #### 检查 逆变化，几乎相等

sns.distplot(df_bias['x2'])
plt.show()
sns.distplot(df_bias2['x2'])
plt.show()

sns.distplot(df_bias['x3'])
plt.show()
sns.distplot(df_bias2['x3'])
plt.show()

########################################################  异常检测模块 #########################################################

#############生成数据
boston = datasets.load_boston()
df = pd.DataFrame(data=boston.data,columns=boston.feature_names)
df['y_label'] = boston.target
ols = sm.OLS(boston.target,boston.data).fit()
mean_squared_error(boston.target,ols.predict(boston.data))
r2_score(boston.target,ols.predict(boston.data))

if_result = OLSInfluence(ols).summary_frame()
sns.scatterplot(if_result['hat_diag'],if_result['cooks_d'])
plt.show()

###########  去掉离群点 ###########
ol_check = OutlierAttr(1,3)
ol_check.fit(df,df.columns[:-1])
df_ot = ol_check.transform(df,df.columns[:-1])['res']

ols = sm.OLS(df_ot['y_label'],df_ot[df.columns[:-1]]).fit()
mean_squared_error(df_ot['y_label'],ols.predict(df_ot[df.columns[:-1]]))
r2_score(df_ot['y_label'],ols.predict(df_ot[df.columns[:-1]]))


###########  去掉高杠杆点 ###########
ol_check2 = OutlierAttr(2,2)
ol_check2.fit(df,df.columns[:-1])
df_hat = ol_check2.transform(df,df.columns[:-1])['res']

ols = sm.OLS(df_hat['y_label'],df_hat[df.columns[:-1]]).fit()
mean_squared_error(df_hat['y_label'],ols.predict(df_hat[df.columns[:-1]]))
r2_score(df_hat['y_label'],ols.predict(df_hat[df.columns[:-1]]))



###########  去强影响点  ###########
ol_check3 = OutlierAttr(3,0.1)
ol_check3.fit(df,df.columns[:-1])
df_ck = ol_check3.transform(df,df.columns[:-1])['res']

ols = sm.OLS(df_ck['y_label'],df_ck[df.columns[:-1]]).fit()
mean_squared_error(df_ck['y_label'],ols.predict(df_ck[df.columns[:-1]]))
r2_score(df_ck['y_label'],ols.predict(df_ck[df.columns[:-1]]))

################################################  删除共线性 #################################################################
df = pd.DataFrame(data=boston.data,columns=boston.feature_names)
df['y_label'] = boston.target

corr1 = CorrAttr(1,0.75)
corr1.fit(df,df.columns[:-1])
corr1.transform(df,df.columns[:-1])['res']

corr2 = CorrAttr(2,10)
corr2.fit(df,df.columns[:-1])
corr2.transform(df,df.columns[:-1])['res']

################################################ Sparse 稀疏变量处理 ########################################################
df = pd.DataFrame(data=boston.data,columns=boston.feature_names)
df['y_label'] = boston.target


sparse = SparseAttr(1,20) ## 是最常见的取值频数和第二常见的取值频数之间的比值 大于20的删掉
sparse.fit(df,df.columns[:-1])
sparse.transform(df,df.columns[:-1])['res']

sparse2 = SparseAttr(2,20) ##样本量与 不同取值数目的比值 大于20的删掉，或者考虑转为 类别特征
sparse2.fit(df,df.columns[:-1])
sparse2.transform(df,df.columns[:-1])['res']

##################################################### Sparse 时间序列  ########################################################
'''
df = df.groupby(['WAFER_ID']).agg(lambda x:list(x)).reset_index()
'''
df = pd.read_csv('files//ts_df.csv')
del df['CHAMBER']
df = df.rename(columns={'TIMESTAMP':'ts','WAFER_ID':'sample_id','AVG_REMOVAL_RATE':'y_label'})

cols = list(df.columns[2:-8])

ts_att = TSproAttr(2,3)
ts_att.fit(df,cols)
ts_att.transform(df,cols)['res']

ts_att1 = TSproAttr(1,'0.5S')
ts_att1.fit(df,cols)
ts_att1.transform(df,cols)['res']


################################################# 分类特征  ############################################
###### 仅字典编码和label编码, 字典编码则需要提供映射关系

diabetes = datasets.load_diabetes()
df = pd.DataFrame(data=diabetes.data,columns=diabetes.feature_names)
df['y_label'] = diabetes.target
df = df.reset_index().rename(columns={'index':'sample_id'})

df['sex1'] = df['sex'].apply(lambda x:'Male' if x>=0 else 'Female')
df['sex'] = df['sex'].apply(lambda x:'Male' if x>=0 else 'Female')

dict_cols={'sex':{'Female':0,'Male':1}}

ctgattr = CtgAttr(1,dict_cols)
ctgattr.fit(df,['sex','sex1'])

ctgattr.transform(df,['sex','sex1'])


############################################### 分类特征  ################################################

diabetes = datasets.load_diabetes()
df = pd.DataFrame(data=diabetes.data,columns=diabetes.feature_names)
df['y_label'] = diabetes.target
df = df.reset_index().rename(columns={'index':'sample_id'})
df['sex'] = df['sex'].apply(lambda x:'Male' if x>=0 else 'Female')

############### one_hot
oh = OneHot(strategy=1)
oh.fit(df,['sex'])
df = oh.transform(df,['sex'])['res']

###############count_encoder
ced = FreqEncoder()
ced.fit(df,['sex'])
df = ced.transform(df,['sex'])['res']

#############  target encoder
tar = TarEncoder()
tar.fit(df,['sex'])
df = tar.transform(df,['sex'])['res']

############################################### 数值特征  ################################################
################ 分桶 ################
num = 10000
x1 = np.random.randint(1,10,(1,num))
x2 = np.random.randint(10,30,(1,num))
x3 = np.random.randint(30,45,(1,num))
x4 = np.random.randint(45,80,(1,num))
x = list(x1[0])+list(x2[0])+list(x3[0])+list(x4[0])

y1 = [0 for i in range(int(num*0.4))]+[1 for i in range(int(num*0.2))]+[2 for i in range(int(num*0.2))]+[3 for i in range(int(num*0.2))]
y2 = [0 for i in range(int(num*0.5))]+[1 for i in range(int(num*0.3))]+[2 for i in range(int(num*0.1))]+[3 for i in range(int(num*0.1))]
y3 = [0 for i in range(int(num*0.4))]+[1 for i in range(int(num*0.3))]+[2 for i in range(int(num*0.2))]+[3 for i in range(int(num*0.1))]
y4 = [0 for i in range(int(num*0.5))]+[1 for i in range(int(num*0.3))]+[2 for i in range(int(num*0.2))]#+[3 for i in range(int(num*0.1))]
y = y1+y2+y3+y4

testdata = pd.DataFrame({"x":x,'x2':x,"y_label":y})

########## 卡方分桶  ###目标是多分类
bukencoder = BukEncoder(4)
bukencoder.fit(testdata,['x','x2'])
testdata = bukencoder.transform(testdata,['x','x2'])['res']

######## 决策树分桶   ###目标是分类
bukencoder2 = BukEncoder(3)
bukencoder2.fit(testdata,['x','x2'])
testdata = bukencoder2.transform(testdata,['x','x2'])['res']

######## best-ks分箱
bukencoder3 = BukEncoder(5,5)
bukencoder3.fit(testdata,['x','x2'])
testdata = bukencoder3.transform(testdata,['x','x2'])['res']

######################## 等距

bukencoder4 = BukEncoder(1,5,1)
bukencoder4.fit(testdata,['x'])
testdata = bukencoder4.transform(testdata,['x'])['res']
testdata
bukencoder5 = BukEncoder(1,5,2) #####仅支持整数
bukencoder5.fit(testdata,['x'])
testdata = bukencoder5.transform(testdata,['x'])['res']
testdata

######################## 等频率

bukencoder6 = BukEncoder(2,5)
bukencoder6.fit(testdata,['x'])
testdata = bukencoder6.transform(testdata,['x'])['res']

###################################################类别 + 数值特征 交叉 #################################################
testdata['x1'] = testdata['x'].apply(lambda x:random.randint(0,1000)/1000)
testdata['x2'] = testdata['x'].apply(lambda x:random.randint(0,100)/100)
testdata['x3'] = testdata['x'].apply(lambda x:random.randint(0,3))
testdata['x4'] = testdata['x'].apply(lambda x:random.randint(0,2))


crossfs = CrossFeatures(2)
crossfs.fit(testdata,['x3','x4'],['x','x1','x2'])
testdata = crossfs.transform(testdata,['x3','x4'],['x','x1','x2'])['res']#['x4_x2_gap1'].unique()


######################################################## 特征选择 ##############################################################
##################### 测试数据
num = 20000
x1 =   [0 for i in range(int(num*0.98))] + [1 for i in range(int(num*0.02))]
x2 =   [random.randint(10,100)/100 +random.random()  for i in range(num)]

y1 =   [random.randint(600,660) +random.random()*10 for i in range(num)] ####x1 的差异与y1无关
y2 =   [random.randint(600,660)/10 +random.random()*5 for _ in range(int(num*0.9))] +  [random.randint(640,660)/10 +random.random()*5  for _ in range(int(num*0.1))] ####x1 的差异与y2有关 ，回归
y3 =   [0for _ in range(int(num*0.95))] +  [1 for _ in range(int(num*0.05))] ####x1 的差异与y3有关  ，分类

df = pd.DataFrame({"x1":x1,'x2':x2,"y1":y1,'y2':y2,'y3':y3})



iris = load_iris()
rfe = RFE(estimator=LogisticRegression(), n_features_to_select=2)
rfe.fit(iris.data, iris.target)
rfe.transform(iris.data)
rfe.get_support()

iris = load_iris()
X, y = iris.data, iris.target

lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(X, y)
sfm = SelectFromModel(lsvc, prefit=True)
