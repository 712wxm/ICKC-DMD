# import seaborn library
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# print(dataset.head())
# load the dataset
# data = sns.load_dataset('tips')
# # view the dataset
# print(data.head(5))
#data = dataset.query('Sampling == 0 and Metric == "F1"')
# # data = dataset
# data = data.groupby(['Method', 'Metric', 'Sampling']).agg({'Value': ['mean']})
# print(data.head(1000000))
# data_bc = dataset.query('Sampling == 1')
# sns.boxplot(x = data['Method'],
#             y = data['Value'],
#             hue = data['Classifier'],
#             palette = 'Paired_r')




# RQ3: multiclass  0无过采样了，1有过采样
# dataset = pd.read_excel('results.xlsx', sheet_name=11)
# data = dataset.query('Sampling == 1') #采样
# sns.boxplot(x = data['Method'],
#             y = data['Value(%)'],
#             hue = data['Classifier'],
#             palette = 'Paired_r')
# #保存两种方法不同的评价指标，说明tfidf比较好一些
# plt.title('TFIDF vs BM25(with Sampling)')
# plt.savefig("TFIDF vs BM25(with Sampling)",dpi=500)

# dataset = pd.read_excel('results.xlsx', sheet_name=11)
# data = dataset.query('Sampling == 0') #未采样
# sns.boxplot(x = data['Method'],
#             y = data['Value(%)'],
#             hue = data['Classifier'],
#             palette = 'Paired_r')
# #保存两种方法不同的评价指标，说明tfidf比较好一些
# plt.title('TFIDF vs BM25(without Sampling)')
# plt.savefig("TFIDF vs BM25(without Sampling)",dpi=500)

# 这两行代码解决 plt 中文显示的问题

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

dataset = pd.read_excel('results.xlsx', sheet_name=14)
data = dataset.query('Sampling==1') #采样了
sns.boxplot(x = data['评价指标'],
            y = data['百分比(%)'],
            hue = data['分类器'],
            palette = 'Paired_r')
plt.title('使用过采样')
plt.savefig("使用过采样",dpi=500)


# dataset = pd.read_excel('results.xlsx', sheet_name=12)
# data = dataset.query('Sampling == 0')#未采样
# sns.boxplot(x = data['Metric'],
#             y = data['Value(%)'],
#             hue = data['Classifier'],
#             palette = 'Paired_r')
# plt.title('without Oversampling')
# plt.savefig("without Oversampling",dpi=500)


# data = dataset.query('Sampling == 1')
# data = data.query('Metric == "AUC"')
# sns.boxplot(x = data['Method'],
#             y = data['Value'],
#             hue = data['n'],
#             palette = 'Greys')

# data = dataset.query('Sampling == 0')
# data = data.query('Metric == "AUC"')
# sns.boxplot(x = data['Method'],
#             y = data['Value'],
#             hue = data['n'],
#             palette = 'Greys')

plt.show()