import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import scipy
from scipy.stats import chi2
import matplotlib.pyplot as plt


def optimal_binning_boundary(x, y):
    '''
        利用决策树获得最优分箱的边界值列表,利用决策树生成的内部划分节点的阈值，作为分箱的边界
    '''
    boundary = []  # 待return的分箱边界值列表

    x = x.values.reshape(-1, 1)
    y = y.values.reshape(-1, 1)

    clf = DecisionTreeClassifier(criterion='entropy',  # “信息熵”最小化准则划分
                                 max_leaf_nodes=6,  # 最大叶子节点数
                                 min_samples_leaf=0.05)  # 叶子节点样本数量最小占比

    clf.fit(x, y)  # 训练决策树

    # tree.plot_tree(clf) #打印决策树的结构图
    # plt.show()

    n_nodes = clf.tree_.node_count  # 决策树的节点数
    children_left = clf.tree_.children_left  # node_count大小的数组，children_left[i]表示第i个节点的左子节点
    children_right = clf.tree_.children_right  # node_count大小的数组，children_right[i]表示第i个节点的右子节点
    threshold = clf.tree_.threshold  # node_count大小的数组，threshold[i]表示第i个节点划分数据集的阈值

    for i in range(n_nodes):
        if children_left[i] != children_right[i]:  # 非叶节点
            boundary.append(threshold[i])

    boundary.sort()

    premise = "str(0) if "
    len_boundary = len(boundary)

    for i in range(len_boundary + 1):
        if i == 0:
            premise += 'x<=%f' % (boundary[i])
        elif i == len_boundary:
            premise += ' else ' + str(i)  # + ' if x>%f '%(boundary[-1])
        else:
            premise += ' else ' + str(i) + ' if x>%f and x<=%f ' % (boundary[i - 1], boundary[i])

    return boundary, premise


def best_ks_box(data, var_name, box_num):
    data = data[[var_name, 'y_label']]
    """
    KS值函数
    """

    def ks_bin(data_, limit):
        g = data_.iloc[:, 1].value_counts()[0]
        b = data_.iloc[:, 1].value_counts()[1]
        data_cro = pd.crosstab(data_.iloc[:, 0], data_.iloc[:, 1])
        data_cro[0] = data_cro[0] / g
        data_cro[1] = data_cro[1] / b
        data_cro_cum = data_cro.cumsum()
        ks_list = abs(data_cro_cum[1] - data_cro_cum[0])
        ks_list_index = ks_list.nlargest(len(ks_list)).index.tolist()
        for i in ks_list_index:
            data_1 = data_[data_.iloc[:, 0] <= i]
            data_2 = data_[data_.iloc[:, 0] > i]
            if len(data_1) >= limit and len(data_2) >= limit:
                break
        return i

    """
    区间选取函数
    """

    def ks_zone(data_, list_):
        list_zone = list()
        list_.sort()
        n = 0
        for val in list_:
            m = sum(data_.iloc[:, 0] <= val) - n
            n = sum(data_.iloc[:, 0] <= val)
            print(val, ' , m:', m, ' n:', n)
            list_zone.append(m)
        # list_zone[i]存放的是list_[i]-list[i-1]之间的数据量的大小
        list_zone.append(50000 - sum(list_zone))
        print('sum ', sum(list_zone[:-1]))
        print('list zone ', list_zone)
        # 选取最大数据量的区间
        max_index = list_zone.index(max(list_zone))
        if max_index == 0:
            rst = [data_.iloc[:, 0].unique().min(), list_[0]]
        elif max_index == len(list_):
            rst = [list_[-1], data_.iloc[:, 0].unique().max()]
        else:
            rst = [list_[max_index - 1], list_[max_index]]
        return rst

    data_ = data.copy()
    limit_ = data.shape[0] / 20  # 总体的5%
    """"
    循环体
    """
    zone = list()
    for i in range(box_num - 1):
        # 找出ks值最大的点作为切点，进行分箱
        ks_ = ks_bin(data_, limit_)
        zone.append(ks_)
        new_zone = ks_zone(data, zone)
        data_ = data[(data.iloc[:, 0] > new_zone[0]) & (data.iloc[:, 0] <= new_zone[1])]

    zone.sort()

    premise = "str(0) if "
    len_zone = len(zone)
    print(len(zone))

    for i in range(len_zone + 1):
        if i == 0:
            premise += 'x<=%f' % (zone[i])
        elif i == len_zone:
            premise += ' else ' + str(i)  # + ' if x>%f '%(boundary[-1])
        else:
            premise += ' else ' + str(i) + ' if x>%f and x<=%f ' % (zone[i - 1], zone[i])

    return zone, premise


def tagcount(series, tags):
    """
    统计该series中不同标签的数量，可以针对多分类
    series:只含有标签的series
    tags:为标签的列表，以实际为准，比如[0,1],[1,2,3]
    """
    result = []
    countseries = series.value_counts()
    for tag in tags:
        try:
            result.append(countseries[tag])
        except:
            result.append(0)
    return result


def ChiMerge3(df, num_split, tags, pvalue_edge=0.1, biggest=10, smallest=3, sample=None):
    """
    df:只包含要分箱的参数列和标签两列
    num_split:初始化时划分的区间个数,适合数据量特别大的时候。
    tags：标签列表，二分类一般为[0,1]。以实际为准。
    pvalue_edge：pvalue的置信度值
    bin：最多箱的数目
    smallest:最少箱的数目
    sample:抽样的数目，适合数据量超级大的情况。可以使用抽样的数据进行分箱。百万以下不需要
    """

    variable = df.columns[0]
    flag = df.columns[1]
    # 进行是否抽样操作
    if sample != None:
        df = df.sample(n=sample)
    else:
        pass

    # 将原始序列初始化为num_split个区间，计算每个区间中每类别的数量，放置在一个矩阵中。方便后面计算pvalue值。
    percent = df[variable].quantile([1.0 * i / num_split for i in range(num_split + 1)],
                                    interpolation="lower").drop_duplicates(keep="last").tolist()
    percent = percent[1:]
    np_regroup = []
    for i in range(len(percent)):
        if i == 0:
            tempdata = tagcount(df[df[variable] <= percent[i]][flag], tags)
            tempdata.insert(0, percent[i])
        elif i == len(percent) - 1:
            tempdata = tagcount(df[df[variable] > percent[i - 1]][flag], tags)
            tempdata.insert(0, percent[i])
        else:
            tempdata = tagcount(df[(df[variable] > percent[i - 1]) & (df[variable] <= percent[i])][flag], tags)
            tempdata.insert(0, percent[i])
        np_regroup.append(tempdata)
    np_regroup = pd.DataFrame(np_regroup)
    np_regroup = np.array(np_regroup)

    # 如果两个区间某一类的值都为0，就会报错。先将这类的区间合并，当做预处理吧
    i = 0
    while (i <= np_regroup.shape[0] - 2):
        check = 0
        for j in range(len(tags)):
            if np_regroup[i, j + 1] == 0 and np_regroup[i + 1, j + 1] == 0:
                check += 1
        """
        这个for循环是为了检查是否有某一个或多个标签在两个区间内都是0，如果是的话，就进行下面的合并。
        """
        if check > 0:
            np_regroup[i, 1:] = np_regroup[i, 1:] + np_regroup[i + 1, 1:]
            np_regroup[i, 0] = np_regroup[i + 1, 0]
            np_regroup = np.delete(np_regroup, i + 1, 0)
            i = i - 1
        i = i + 1

    # 对相邻两个区间进行置信度计算
    chi_table = np.array([])
    for i in np.arange(np_regroup.shape[0] - 1):
        temparray = np_regroup[i:i + 2, 1:]
        pvalue = scipy.stats.chi2_contingency(temparray, correction=False)[1]
        chi_table = np.append(chi_table, pvalue)
    temp = max(chi_table)

    # 把pvalue最大的两个区间进行合并。注意的是，这里并没有合并一次就重新循环计算相邻区间的pvalue，而是只更新影响到的区间。
    while (1):
        # 终止条件，可以根据自己的期望定制化
        if (len(chi_table) <= (biggest - 1) and temp <= pvalue_edge):
            break
        if len(chi_table) < smallest:
            break

        num = np.argwhere(chi_table == temp)
        for i in range(num.shape[0] - 1, -1, -1):
            chi_min_index = num[i][0]
            np_regroup[chi_min_index, 1:] = np_regroup[chi_min_index, 1:] + np_regroup[chi_min_index + 1, 1:]
            np_regroup[chi_min_index, 0] = np_regroup[chi_min_index + 1, 0]
            np_regroup = np.delete(np_regroup, chi_min_index + 1, 0)

            # 最大pvalue在最后两个区间的时候，只需要更新一个，删除最后一个。大家可以画图，很容易明白
            if (chi_min_index == np_regroup.shape[0] - 1):
                temparray = np_regroup[chi_min_index - 1:chi_min_index + 1, 1:]
                chi_table[chi_min_index - 1] = scipy.stats.chi2_contingency(temparray, correction=False)[1]
                chi_table = np.delete(chi_table, chi_min_index, axis=0)

            # 最大pvalue是最先两个区间的时候，只需要更新一个，删除第一个。
            elif (chi_min_index == 0):
                temparray = np_regroup[chi_min_index:chi_min_index + 2, 1:]
                chi_table[chi_min_index] = scipy.stats.chi2_contingency(temparray, correction=False)[1]
                chi_table = np.delete(chi_table, chi_min_index + 1, axis=0)

            # 最大pvalue在中间的时候，影响和前后区间的pvalue，需要更新两个值。
            else:
                # 计算合并后当前区间与前一个区间的pvalue替换
                temparray = np_regroup[chi_min_index - 1:chi_min_index + 1, 1:]
                chi_table[chi_min_index - 1] = scipy.stats.chi2_contingency(temparray, correction=False)[1]
                # 计算合并后当前与后一个区间的pvalue替换
                temparray = np_regroup[chi_min_index:chi_min_index + 2, 1:]
                chi_table[chi_min_index] = scipy.stats.chi2_contingency(temparray, correction=False)[1]
                # 删除替换前的pvalue
                chi_table = np.delete(chi_table, chi_min_index + 1, axis=0)

        # 更新当前最大的相邻区间的pvalue
        temp = max(chi_table)

    print("*" * 40)
    print("最终相邻区间的pvalue值为：")
    print(chi_table)
    print("*" * 40)

    # 把结果保存成一个数据框。
    """  
    可以根据自己的需求定制化。我保留两个结果。
    1. 显示分割区间，和该区间内不同标签的数量的表
    2. 为了方便pandas对该参数处理，把apply的具体命令打印出来。方便直接对数据集处理。
        serise.apply(lambda x:XXX)中XXX的位置
    """
    # 将结果整合到一个表中，即上述中的第一个
    interval = []
    interval_num = np_regroup.shape[0]
    for i in range(interval_num):
        if i == 0:
            interval.append('x<=%f' % (np_regroup[i, 0]))
        elif i == interval_num - 1:
            interval.append('x>%f' % (np_regroup[i - 1, 0]))
        else:
            interval.append('x>%f and x<=%f' % (np_regroup[i - 1, 0], np_regroup[i, 0]))

    result = pd.DataFrame(np_regroup)
    result[0] = interval
    result.columns = ['interval'] + tags

    # 整理series的命令，即上述中的第二个
    premise = "str(0) if "
    length_interval = len(interval)
    for i in range(length_interval):
        if i == length_interval - 1:
            premise = premise[:-4]
            break
        premise = premise + interval[i] + " else " + 'str(%d+1)' % i + " if "

    return result, premise


if __name__ =='__main()':
    #if __name__ =='__main()':
    #构造一个有40000数据量的数据
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

    testdata = pd.DataFrame({"x":x,"y_label":y})
    #打乱顺序，其实没必要，分箱的时候会重新对x进行排序
    #testdata = testdata.sample(frac=1)

    boundary,premise = optimal_binning_boundary(testdata['x'], testdata['y_label'])
    zone,premise = best_ks_box(testdata, 'x', 5)

    ####卡方
    testdata.groupby(by='x')['y_label'].mean().sort_index().plot()
    plt.show()

    ChiMerge3(testdata,100,[0,1,2,3],pvalue_edge=0.05)

    result,sentence = ChiMerge3(testdata,100,[0,1,2,3],pvalue_edge=0.01)
    testdata['x'] = testdata['x'].apply(lambda x :eval(sentence) )

