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
from sklearn.naive_bayes import MultinomialNB
from imblearn.over_sampling import SMOTE

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score

import warnings
warnings.filterwarnings("ignore")

# implements TF-IDF

def main():
    
    pd.set_option('display.max_columns', None)
    np.random.RandomState(0)

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
    
    file = open('NPChunks_bias_corrected_final_result.txt', 'w')
    
    for top_n_class in [2, 4]:
        file.write('\n=================\n')
        file.write(f'n = {top_n_class}\n')
        print(f'n = {top_n_class}\n')
        
        classCounts_sorted = sorted(classCounts, key = lambda x:x['count'], reverse = True)[0:top_n_class]
        classCounts_top_n = [item['name'] for item in classCounts_sorted]
        
        trainAndTestSetFiltered = trainAndTestSet[trainAndTestSet['name'].isin(classCounts_top_n)]
    
    
        text_corpus = trainAndTestSetFiltered['description'].values
        text_corpus = utils.removeURLandCitationBulk(text_corpus)
        
        # print(text_corpus)
        # print("######")
        
        out = utils.filterNPsFromCorpus(text_corpus)
        text_corpus = out[0]
        
        
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
        
        numOfColumns = len(trainAndTestSetFiltered.columns)
        print(numOfColumns)
        
        
        sm = SMOTE(random_state = 2, sampling_strategy='auto')
        X_train_res, y_train_res = sm.fit_resample(trainAndTestSetFiltered.iloc[:, 4:numOfColumns], trainAndTestSetFiltered['name'].ravel())
        
        
        X_train_res_df = pd.DataFrame(np.array(X_train_res)).add_prefix('column')
        y_train_res_df = pd.DataFrame(np.array(y_train_res), columns=['name'])
        
        trainAndTestSetFiltered = pd.concat([ X_train_res_df.reset_index(drop=True), y_train_res_df.reset_index(drop=True) ], axis=1)
            
        skf = StratifiedKFold(n_splits=5)
        target = trainAndTestSetFiltered.loc[:,'name']

        train = []
        test = []
        
        for train_index, test_index in skf.split(trainAndTestSetFiltered, target):
            train.append(trainAndTestSetFiltered.iloc[train_index])
            test.append(trainAndTestSetFiltered.iloc[test_index])
            
        for item in ['knn', 'nn','nb', 'svm', 'dt','rf']:
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
            
                if item == 'knn': clf = KNeighborsClassifier().fit(train[index].iloc[:, 0:(numOfColumns-1)], train[index]['name'])
                if item == 'nn': clf = MLPClassifier().fit(train[index].iloc[:, 0:(numOfColumns-1)], train[index]['name'])
                if item == 'nb': clf = GaussianNB().fit(train[index].iloc[:, 0:(numOfColumns-1)], train[index]['name'])
                if item == 'svm': clf = svm.SVC(probability=True).fit(train[index].iloc[:, 0:(numOfColumns-1)], train[index]['name'])
                if item == 'dt': clf = DecisionTreeClassifier().fit(train[index].iloc[:, 0:(numOfColumns-1)], train[index]['name'])
                if item == 'rf': clf = RandomForestClassifier().fit(train[index].iloc[:, 0:(numOfColumns-1)], train[index]['name'])
                
                
                predicted = clf.predict(test[index].iloc[:, 0:(numOfColumns-1)])
                output = classification_report(test[index]['name'], predicted, output_dict =  True)
                probs = clf.predict_proba(test[index].iloc[:, 0:(numOfColumns-1)])

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
        
    file.close()

if __name__ == "__main__":
    main()