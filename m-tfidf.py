from numpy.ma import count
import pandas as pd
from pandas import DataFrame
import gensim
from gensim.parsing.preprocessing import preprocess_documents
import utils
from gensim.models.coherencemodel import CoherenceModel
import csv
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import numpy as np, random
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE

from sklearn.metrics import average_precision_score, precision_recall_curve, auc

from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier

import warnings, random
warnings.filterwarnings("ignore")

# implements TF-IDF

def main():
    
    pd.set_option('display.max_columns', None)
    np.random.RandomState(0)
    random.seed(0)

    dfTactics = pd.read_excel('attack-data.xlsx', sheet_name=0)
    dfTechniques = pd.read_excel('attack-data.xlsx', sheet_name=2)
    dfProcedures = pd.read_excel('attack-data.xlsx', sheet_name=3)

    dfTacticsCut = dfTactics.loc[:, ['ID', 'name', 'description']]
    dfTacticsCut['type'] = 'tactics'
    dfTechniquesCut = dfTechniques.loc[:, ['ID', 'name', 'description']]
    dfTechniquesCut['type'] = 'techniques'

    dfTechniqueProcedureMerged = pd.merge(dfTechniques, dfProcedures, left_on='ID', right_on='target ID')

    dfProceduresCut = dfTechniqueProcedureMerged.loc[:, ['source ID', 'name', 'mapping description']]
    dfProceduresCut['ID'] = dfProceduresCut['source ID']
    dfProceduresCut['description'] = dfProceduresCut['mapping description']
    dfProceduresCut['type'] = 'example'
    dfProceduresCut = dfProceduresCut.loc[:, ['ID', 'name', 'description', 'type']]

    dataframe = pd.concat([dfTacticsCut, dfTechniquesCut, dfProceduresCut], ignore_index=True)
    
    
    trainAndTestSet = dataframe.loc[dataframe['type'] == 'example']
    trainAndTestSet['name'] = trainAndTestSet['name'].apply(utils.splitTechniqueName)

    techniqueNamesWithLessThanFiveExamples = []
    trainAndTestSetGrouped = trainAndTestSet.groupby('name')
    
    classCounts = []
    
    for name,group in trainAndTestSetGrouped:
        classCounts.append({ 'name' : f'{name}', 'count' : group.shape[0]})
        if group.shape[0] < 30:
            techniqueNamesWithLessThanFiveExamples.append(name)
    
    
    file = open('tfidf_final_result.txt', 'w')
    
    for top_n_class in [2, 4, 8]:
        file.write('\n=================\n')
        file.write(f'n = {top_n_class}\n')
        print(f'n = {top_n_class}\n')
        classCounts_sorted = sorted(classCounts, key = lambda x:x['count'], reverse = True)[0:top_n_class]
        classCounts_top_n = [item['name'] for item in classCounts_sorted]
        
        trainAndTestSetFiltered = trainAndTestSet[trainAndTestSet['name'].isin(classCounts_top_n)]
        
        
        
        text_corpus = trainAndTestSetFiltered['description'].values
        text_corpus = utils.removeURLandCitationBulk(text_corpus)
        
        l = random.sample(range(1,len(text_corpus)), 100)
        print(l)
        
        file2 = open('svo.csv', 'w')
        
        for item in l:
            file2.write(f'{text_corpus[item]} ### {utils.extractBoW(text_corpus[item])}\n')
        
        file2.close()
        
        processed_corpus = preprocess_documents(text_corpus)
        
        list = []
        for item in processed_corpus:
            text = ' '.join(item)
            list.append(text.strip())
        
        
        trainAndTestSetFiltered['description'] = list 
        
        vectorizer = TfidfVectorizer(use_idf=True)
        vectors = vectorizer.fit_transform(trainAndTestSetFiltered['description'])
        feature_names = vectorizer.get_feature_names()
        feature_names = ['feature-' + feature_name for feature_name in feature_names]
        dense = vectors.todense()
        denselist = dense.tolist()
        df = pd.DataFrame(denselist, columns=feature_names)
        trainAndTestSetFiltered = pd.concat([trainAndTestSetFiltered.reset_index(drop=True), df.reset_index(drop=True)], axis=1)
        
        # print(trainAndTestSetFiltered.shape)
            
        skf = StratifiedKFold(n_splits=5)
        target = trainAndTestSetFiltered.loc[:,'name']

        train = []
        test = []

        for train_index, test_index in skf.split(trainAndTestSetFiltered, target):
            train.append( trainAndTestSetFiltered.iloc[train_index] )
            test.append( trainAndTestSetFiltered.iloc[test_index] )
        
        for item in ['GaussianNB', 'MLP', 'KNN', 'SVM', 'RF','DT','AdaBoost','GBDT']:
            file.write('\n###################\n')
            file.write(f'classifier: {item}')
            print(f'classifier: {item}')
            
            accuracy = []
            precision_m = []
            precision_w = []
            recall_m = []
            recall_w = []
            f1_m = []
            f1_w = []
            auc = []
        
            for index in range(0, 5):
                numOfColumns = len(train[index].columns)
                
                clf = None
                # 高斯朴素贝叶斯
                if item == 'GaussianNB': clf = GaussianNB().fit(train[index].iloc[:, 0:(numOfColumns - 1)],train[index]['name'])
                # 多层感知机
                if item == 'MLP': clf = MLPClassifier().fit(train[index].iloc[:, 0:(numOfColumns - 1)],train[index]['name'])
                # knn
                if item == 'KNN': clf = KNeighborsClassifier().fit(train[index].iloc[:, 0:(numOfColumns - 1)],train[index]['name'])
                # 支持向量机
                if item == 'SVM': clf = svm.SVC(probability=True).fit(train[index].iloc[:, 0:(numOfColumns - 1)],train[index]['name'])
                # 随机森林
                if item == 'RF': clf = RandomForestClassifier().fit(train[index].iloc[:, 0:(numOfColumns - 1)],train[index]['name'])
                # 决策树
                if item == 'DT': clf = DecisionTreeClassifier().fit(train[index].iloc[:, 0:(numOfColumns - 1)],train[index]['name'])
                # AdaBoost
                if item == 'AdaBoost': clf = AdaBoostClassifier().fit(train[index].iloc[:, 0:(numOfColumns - 1)],train[index]['name'])
                # gbdt
                if item == 'GBDT': clf = GradientBoostingClassifier().fit(train[index].iloc[:, 0:(numOfColumns - 1)],train[index]['name'])
                
                predicted = clf.predict(test[index].iloc[:, 4:(numOfColumns)])
                output = classification_report(test[index]['name'], predicted, output_dict =  True)
                probs = clf.predict_proba(test[index].iloc[:, 4:(numOfColumns)])
                
                if top_n_class == 2: 
                    auc.append(roc_auc_score( test[index]['name'] , probs[:,1]))
                else: 
                    auc.append(roc_auc_score( test[index]['name'] , probs , multi_class='ovr', average='weighted'))
                
                accuracy.append(output['accuracy'])
                precision_m.append(output['macro avg']['precision'])
                precision_w.append(output['weighted avg']['precision'])
                recall_m.append(output['macro avg']['recall'])
                recall_w.append(output['weighted avg']['recall'])
                f1_m.append(output['macro avg']['f1-score'])
                f1_w.append(output['weighted avg']['f1-score'])

            file.write(f'accuracy: {sum(accuracy)/5}\n')
            file.write(f'precision macro: {sum(precision_m)/5}\n') 
            file.write(f'precision weighted: {sum(precision_w)/5}\n') 
            file.write(f'recall macro: {sum(recall_m)/5}\n') 
            file.write(f'recall weighted: {sum(recall_w)/5}\n') 
            file.write(f'f1 macro: {sum(f1_m)/5}\n') 
            file.write(f'f1 weighted: {sum(f1_w)/5}\n')  
            file.write(f'auc: {sum(auc)/5}\n')
            file.write('###################\n')

    file.write('=================\n')
    file.close()
    
    # implement word embedding 
    # prepare oracle for svo extraction
    # take the five data points for precision recall for drawing the roc curve 
    # take the true positives and false positives data 
    # report the paper's performance with our observed performance

if __name__ == "__main__":
    main()