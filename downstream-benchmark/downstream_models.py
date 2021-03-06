# ==============================================================================
# File: downstream_modes.py
# Author: Vraj Shah
# Revisions by: Francisco Cornejo-Garcia
# Description: Set up downstream models for data prep
# ==============================================================================

# Load models
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn import tree
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from math import sqrt
import sys
maxintval = sys.maxsize
Hcurstate = 100



# Logistic Regression Classifier ===============================================

def LogRegClassifier(data1, y):
    # Split training data
    X_train, X_test, y_train, y_test = train_test_split(data1, y, test_size = 0.2, 
                                                        random_state = Hcurstate)
    X_train_new = X_train.reset_index(drop = True)
    y_train_new = y_train.reset_index(drop = True)
    
    X_train_new = X_train_new.values
    y_train_new = y_train_new.values

    k = 5
    kf = KFold(n_splits = k, random_state = Hcurstate)
    avg_train_acc, avg_test_acc = 0, 0

    val_arr = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]

    avgsc_lst, avgsc_train_lst, avgsc_hld_lst = [], [], []
    avgsc, avgsc_train, avgsc_hld = 0, 0, 0

    for train_index, test_index in kf.split(X_train_new):
        X_train_cur, X_test_cur = X_train_new[train_index], X_train_new[test_index]
        y_train_cur, y_test_cur = y_train_new[train_index], y_train_new[test_index]
        X_train_train, X_val, y_train_train, y_val = train_test_split(X_train_cur, y_train_cur, 
                                                                      test_size = 0.25, random_state = Hcurstate)

        # print(X_train_train.shape)
        # print(X_val.shape)
        
        bestPerformingModel = LogisticRegression(penalty='l2', C = 1, random_state = Hcurstate)
        bestscore = 0
        for val in val_arr:
            clf = LogisticRegression(penalty = 'l2',C = val,random_state = Hcurstate)
            clf.fit(X_train_train, y_train_train)
            sc = clf.score(X_val, y_val)

            if bestscore < sc:
                bestscore = sc
                bestPerformingModel = clf

        bscr_train = bestPerformingModel.score(X_train_cur, y_train_cur)
        bscr = bestPerformingModel.score(X_test_cur, y_test_cur)
        bscr_hld = bestPerformingModel.score(X_test, y_test)

        avgsc_train_lst.append(bscr_train)
        avgsc_lst.append(bscr)
        avgsc_hld_lst.append(bscr_hld)

        avgsc_train = avgsc_train + bscr_train    
        avgsc = avgsc + bscr
        avgsc_hld = avgsc_hld + bscr_hld

        # print(bscr_train)
        # print(bscr)
        # print(bscr_hld)
    
    print('5 fold Train, Validation, and Test Accuracies:')
    print(avgsc_train_lst)
    print(avgsc_lst)
    print(avgsc_hld_lst)

    print('Avg Train, Validation, and Test Accuracies:')    
    print(avgsc_train / k)
    print(avgsc / k)
    print(avgsc_hld / k)
        
    y_pred = bestPerformingModel.predict(X_test)
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    
    return avgsc_train_lst, avgsc_lst, avgsc_hld_lst, cnf_matrix



# Random Forest Classifier =====================================================

def RandForestClassifier(data1, y):
    X_train, X_test, y_train, y_test = train_test_split(data1, y, test_size = 0.2, random_state = Hcurstate)
    
    X_train_new = X_train.reset_index(drop = True)
    y_train_new = y_train.reset_index(drop = True)
    
    X_train_new = X_train_new.values
    y_train_new = y_train_new.values

    k = 5
    kf = KFold(n_splits = k, random_state = Hcurstate)
    avg_train_acc, avg_test_acc = 0,0

    n_estimators_grid = [5, 25, 50, 75, 100, 500]
    max_depth_grid = [5, 10, 25, 50, 100, 500]

    avgsc_lst, avgsc_train_lst, avgsc_hld_lst = [], [], []
    avgsc, avgsc_train, avgsc_hld = 0, 0, 0

    for train_index, test_index in kf.split(X_train_new):
        X_train_cur, X_test_cur = X_train_new[train_index], X_train_new[test_index]
        y_train_cur, y_test_cur = y_train_new[train_index], y_train_new[test_index]
        X_train_train, X_val, y_train_train, y_val = train_test_split(X_train_cur, y_train_cur, 
                                                                      test_size=0.25, random_state = Hcurstate)

        # print(X_train_train.shape)
        # print(X_val.shape)            
        
        bestPerformingModel = RandomForestClassifier(n_estimators = 10, max_depth = 5, random_state = Hcurstate)
        bestscore = 0
        for ne in n_estimators_grid:
            for md in max_depth_grid:
                clf = RandomForestClassifier(n_estimators = ne, max_depth = md, random_state = Hcurstate)
                clf.fit(X_train_train, y_train_train)
                sc = clf.score(X_val, y_val)

                if bestscore < sc:
                    bestscore = sc
                    bestPerformingModel = clf

        bscr_train = bestPerformingModel.score(X_train_cur, y_train_cur)
        bscr = bestPerformingModel.score(X_test_cur, y_test_cur)
        bscr_hld = bestPerformingModel.score(X_test, y_test)

        avgsc_train_lst.append(bscr_train)
        avgsc_lst.append(bscr)
        avgsc_hld_lst.append(bscr_hld)

        avgsc_train = avgsc_train + bscr_train    
        avgsc = avgsc + bscr
        avgsc_hld = avgsc_hld + bscr_hld

        # print(bscr_train)
        # print(bscr)
        # print(bscr_hld)
    
    print('5 fold Train, Validation, and Test Accuracies:')
    print(avgsc_train_lst)
    print(avgsc_lst)
    print(avgsc_hld_lst)
    
    print('Avg Train, Validation, and Test Accuracies:')    
    print(avgsc_train / k)
    print(avgsc / k)
    print(avgsc_hld / k)
        
    y_pred = bestPerformingModel.predict(X_test)
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    
    return avgsc_train_lst, avgsc_lst, avgsc_hld_lst, cnf_matrix



# Linear Regression Classifier =================================================

def LinearRegression(data1, y):
    X_train, X_test, y_train, y_test = train_test_split(data1, y, test_size = 0.2, random_state = Hcurstate)

    X_train_new = X_train.reset_index(drop = True)
    y_train_new = y_train.reset_index(drop = True)
    
    X_train_new = X_train_new.values
    y_train_new = y_train_new.values

    k = 5
    kf = KFold(n_splits = k, random_state = Hcurstate)
    avg_train_acc, avg_test_acc = 0, 0

    val_arr = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]

    avgsc_lst, avgsc_train_lst, avgsc_hld_lst = [], [], []
    avgsc, avgsc_train, avgsc_hld = 0, 0, 0

    for train_index, test_index in kf.split(X_train_new):
        X_train_cur, X_test_cur = X_train_new[train_index], X_train_new[test_index]
        y_train_cur, y_test_cur = y_train_new[train_index], y_train_new[test_index]
        X_train_train, X_val, y_train_train, y_val = train_test_split(X_train_cur, y_train_cur, 
                                                                      test_size = 0.25, random_state = Hcurstate)

        # print(X_train_train.shape)
        # print(X_val.shape)            
        
        bestPerformingModel = Ridge(alpha = 1.0, random_state = Hcurstate)
        bestscore = maxintval

        for val in val_arr:
            clf = Ridge(alpha = val,random_state = Hcurstate)
            clf = clf.fit(X_train_train, y_train_train)
            y_pred = clf.predict(X_val)
            sc = sqrt(mean_squared_error(y_pred, y_val))
            if bestscore > sc:
                bestscore = sc
                bestPerformingModel = clf


        y_pred = bestPerformingModel.predict(X_train_cur)
        bscr_train = sqrt(mean_squared_error(y_pred, y_train_cur))
        
        y_pred = bestPerformingModel.predict(X_test_cur)
        bscr = sqrt(mean_squared_error(y_pred, y_test_cur))
        
        y_pred = bestPerformingModel.predict(X_test)
        bscr_hld = sqrt(mean_squared_error(y_pred, y_test))

        avgsc_train_lst.append(bscr_train)
        avgsc_lst.append(bscr)
        avgsc_hld_lst.append(bscr_hld)

        avgsc_train = avgsc_train + bscr_train    
        avgsc = avgsc + bscr
        avgsc_hld = avgsc_hld + bscr_hld

        # print(bscr_train)
        # print(bscr)
        # print(bscr_hld)
    

    print('5-fold Train, Validation, and Test loss:')
    print(avgsc_train_lst)
    print(avgsc_lst)
    print(avgsc_hld_lst)
    
    print('Avg Train, Validation, and Test loss:')    
    print(avgsc_train / k)
    print(avgsc / k)
    print(avgsc_hld / k)
    
    return avgsc_train_lst, avgsc_lst, avgsc_hld_lst



# Random Forest Regressor ======================================================

def RandForestRegressor(data1, y):
    X_train, X_test,y_train,y_test = train_test_split(data1, y, test_size=0.2, random_state = Hcurstate)

    X_train_new = X_train.reset_index(drop = True)
    y_train_new = y_train.reset_index(drop = True)
    
    X_train_new = X_train_new.values
    y_train_new = y_train_new.values

    k = 5
    kf = KFold(n_splits = k, random_state = Hcurstate)
    avg_train_acc, avg_test_acc = 0, 0

    n_estimators_grid = [5, 25, 50, 75, 100, 500]
    max_depth_grid = [5, 10, 25, 50, 100, 500]

    avgsc_lst, avgsc_train_lst, avgsc_hld_lst = [], [], []
    avgsc, avgsc_train, avgsc_hld = 0, 0, 0

    for train_index, test_index in kf.split(X_train_new):   
        X_train_cur, X_test_cur = X_train_new[train_index], X_train_new[test_index]
        y_train_cur, y_test_cur = y_train_new[train_index], y_train_new[test_index]
        X_train_train, X_val, y_train_train, y_val = train_test_split(X_train_cur, y_train_cur, 
                                                                      test_size = 0.25, random_state = Hcurstate)

        # print(X_train_train.shape)
        # print(X_val.shape)            
        
        bestPerformingModel = RandomForestRegressor(n_estimators = 10, max_depth = 5, random_state = Hcurstate)
        bestscore = maxintval
        for ne in n_estimators_grid:
            for md in max_depth_grid:
                clf = RandomForestRegressor(n_estimators = ne, max_depth = md, random_state = Hcurstate)
                clf = clf.fit(X_train_train, y_train_train)
                
                y_pred = clf.predict(X_val)
                sc = sqrt(mean_squared_error(y_pred, y_val))                
                sc = clf.score(X_val, y_val)

                if bestscore > sc:
                    bestscore = sc
                    bestPerformingModel = clf

        y_pred = bestPerformingModel.predict(X_train_cur)
        bscr_train = sqrt(mean_squared_error(y_pred, y_train_cur))
        
        y_pred = bestPerformingModel.predict(X_test_cur)
        bscr = sqrt(mean_squared_error(y_pred, y_test_cur))
        
        y_pred = bestPerformingModel.predict(X_test)
        bscr_hld = sqrt(mean_squared_error(y_pred, y_test))

        avgsc_train_lst.append(bscr_train)
        avgsc_lst.append(bscr)
        avgsc_hld_lst.append(bscr_hld)

        avgsc_train = avgsc_train + bscr_train    
        avgsc = avgsc + bscr
        avgsc_hld = avgsc_hld + bscr_hld

        # print(bscr_train)
        # print(bscr)
        # print(bscr_hld)
    
    print('5-fold Train, Validation, and Test loss:')
    print(avgsc_train_lst)
    print(avgsc_lst)
    print(avgsc_hld_lst)
    
    print('Avg Train, Validation, and Test loss:')    
    print(avgsc_train / k)
    print(avgsc / k)
    print(avgsc_hld / k)

    y_pred = bestPerformingModel.predict(X_test)
    
    return avgsc_train_lst, avgsc_lst, avgsc_hld_lst



# MLP Regressorr ===============================================================

def MLPRegressorr(data1, y):
    X_train, X_test,y_train,y_test = train_test_split(data1,y, test_size = 0.2,random_state = Hcurstate)

    X_train_new = X_train.reset_index(drop = True)
    y_train_new = y_train.reset_index(drop = True)
    
    X_train_new = X_train_new.values
    y_train_new = y_train_new.values

    k = 5
    kf = KFold(n_splits = k,random_state = Hcurstate)
    avg_train_acc, avg_test_acc = 0, 0

    n_estimators_grid = [5, 25, 50, 75, 100, 500]
    max_depth_grid = [5, 10, 25, 50, 100, 500]

    avgsc_lst, avgsc_train_lst, avgsc_hld_lst = [], [], []
    avgsc, avgsc_train, avgsc_hld = 0, 0, 0

    for train_index, test_index in kf.split(X_train_new):      
        X_train_cur, X_test_cur = X_train_new[train_index], X_train_new[test_index]
        y_train_cur, y_test_cur = y_train_new[train_index], y_train_new[test_index]
        X_train_train, X_val, y_train_train, y_val = train_test_split(X_train_cur, y_train_cur, 
                                                                      test_size = 0.25, random_state = Hcurstate)

        # print(X_train_train.shape)
        # print(X_val.shape)            
        
        bestPerformingModel = MLPRegressor(hidden_layer_sizes=(100, 100), max_iter = 300, random_state = Hcurstate)
        bestPerformingModel = bestPerformingModel.fit(X_train, y_train)
        
        # print(bestPerformingModel.n_layers_)

        y_pred = bestPerformingModel.predict(X_train_cur)
        bscr_train = sqrt(mean_squared_error(y_pred, y_train_cur))
        
        y_pred = bestPerformingModel.predict(X_test_cur)
        bscr = sqrt(mean_squared_error(y_pred, y_test_cur))
        
        y_pred = bestPerformingModel.predict(X_test)
        bscr_hld = sqrt(mean_squared_error(y_pred, y_test))

        avgsc_train_lst.append(bscr_train)
        avgsc_lst.append(bscr)
        avgsc_hld_lst.append(bscr_hld)

        avgsc_train = avgsc_train + bscr_train    
        avgsc = avgsc + bscr
        avgsc_hld = avgsc_hld + bscr_hld

        # print(bscr_train)
        # print(bscr)
        # print(bscr_hld)
    
    print('5-fold Train, Validation, and Test loss:')
    print(avgsc_train_lst)
    print(avgsc_lst)
    print(avgsc_hld_lst)
    
    print('Avg Train, Validation, and Test loss:')    
    print(avgsc_train / k)
    print(avgsc / k)
    print(avgsc_hld / k)

    y_pred = bestPerformingModel.predict(X_test)
    
    return avgsc_train_lst, avgsc_lst, avgsc_hld_lst



# MLP Classifierr ==============================================================

def MLPClassifierr(data1,y): 
    X_train, X_test, y_train, y_test = train_test_split(data1, y, test_size = 0.2, random_state = Hcurstate)

    X_train_new = X_train.reset_index(drop = True)
    y_train_new = y_train.reset_index(drop = True)
    
    X_train_new = X_train_new.values
    y_train_new = y_train_new.values

    k = 5
    kf = KFold(n_splits = k,random_state = Hcurstate)
    avg_train_acc, avg_test_acc = 0, 0

    n_estimators_grid = [5, 25, 50, 75, 100, 500]
    max_depth_grid = [5, 10, 25, 50, 100, 500]

    avgsc_lst, avgsc_train_lst, avgsc_hld_lst = [], [], []
    avgsc, avgsc_train, avgsc_hld = 0, 0, 0

    for train_index, test_index in kf.split(X_train_new):     
        X_train_cur, X_test_cur = X_train_new[train_index], X_train_new[test_index]
        y_train_cur, y_test_cur = y_train_new[train_index], y_train_new[test_index]
        X_train_train, X_val, y_train_train, y_val = train_test_split(X_train_cur, y_train_cur, 
                                                                    test_size=0.25, random_state = Hcurstate)

        # print(X_train_train.shape)
        # print(X_val.shape)            
        
        bestPerformingModel = MLPClassifier(hidden_layer_sizes = (100, 100), max_iter = 300, random_state = Hcurstate)
        bestPerformingModel = bestPerformingModel.fit(X_train, y_train)
        
        bscr_train = bestPerformingModel.score(X_train_cur, y_train_cur)
        bscr = bestPerformingModel.score(X_test_cur, y_test_cur)
        bscr_hld = bestPerformingModel.score(X_test, y_test)

        avgsc_train_lst.append(bscr_train)
        avgsc_lst.append(bscr)
        avgsc_hld_lst.append(bscr_hld)

        avgsc_train = avgsc_train + bscr_train    
        avgsc = avgsc + bscr
        avgsc_hld = avgsc_hld + bscr_hld

        # print(bscr_train)
        # print(bscr)
        # print(bscr_hld)
    
    print('5-fold Train, Validation, and Test Accuracies:')
    print(avgsc_train_lst)
    print(avgsc_lst)
    print(avgsc_hld_lst)
    
    print('Avg Train, Validation, and Test Accuracies:')    
    print(avgsc_train / k)
    print(avgsc / k)
    print(avgsc_hld / k)

    y_pred = bestPerformingModel.predict(X_test)
    
    return avgsc_train_lst, avgsc_lst, avgsc_hld_lst
