#coding:utf8

import numpy as np
from sklearn import preprocessing
from time import time
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
from sklearn.cluster import KMeans


path = '/home/ysd/data/装维互联网数据20171019/out4.txt'

array = np.loadtxt(path,dtype=np.str,delimiter=',')
id = array[0:,0].astype(np.int)
level = array[0:,1].astype(np.int)
level_score = array[0:,2].astype(np.float)

feature = array[0:,3:].astype(np.float)

#print id, level, level_score, feature

feature_scale = preprocessing.scale(feature)
#print feature_scale

min_max_scaler = preprocessing.MinMaxScaler()
feature_minMax = min_max_scaler.fit_transform(feature)
print feature_minMax

n_samples, n_features = feature_minMax.shape

print '员工数：', n_samples, '特征数:', n_features

#调用kmeans类
clf = KMeans(n_clusters=5)
s = clf.fit(feature_minMax)
print s

#9个中心
print clf.cluster_centers_
ax=plt.gca()
ax.set_xticks(np.linspace(0,13,14))
#ax.set_xticklabels( (u'装机次数',u'装机耗时',u'装机均价',u'修障次数',u'修障耗时',u'修障宽带占比',u'营销次数',u'营销均价',u'营销天翼占比',u'营销宽带占比',u'延伸服务次数',u'延伸服务均价',u'活动次数',u'其他次数'))
ax.set_xticklabels( (u'装机次数',u'修障次数',u'营销次数',u'延伸服务次数',u'活动次数',u'其他次数',u'装机耗时',u'装机均价',u'修障耗时',u'修障宽带占比',u'营销均价',u'营销天翼占比',u'营销宽带占比',u'延伸服务均价'))
plt.plot(clf.cluster_centers_.transpose())
plt.grid(True)
plt.show()

#每个样本所属的簇
print clf.labels_

#用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
print clf.inertia_