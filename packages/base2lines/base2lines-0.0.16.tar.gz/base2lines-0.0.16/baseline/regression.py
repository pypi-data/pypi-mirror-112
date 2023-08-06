from sklearn.pipeline import *
from sklearn.naive_bayes import *
from sklearn.preprocessing import *
from sklearn.svm import *
from sklearn.decomposition import *
from sklearn.model_selection import *
from sklearn.linear_model import *
from sklearn.compose import *
from sklearn.feature_extraction.text import *
from sklearn.impute import *
from sklearn.ensemble import *
from sklearn.metrics import *
from sklearn.neural_network import *
from xgboost import *
import numpy as np
import pandas as pd

class Regression:
    """
    Benchmarks dataset on various regression algorithms
    """
    def __init__(self) -> None:
        pass
    def regressor(self,dataset,resultantColumn):
        """
        takes dataset and resultant columns as input and returns dictionary of various algorithms and their explained scores
        """
        dataset = pd.DataFrame(dataset)
        dataset[resultantColumn] = pd.to_numeric(dataset[resultantColumn],errors='coerce')
           
        dataset[resultantColumn].fillna(dataset[resultantColumn].mean(), inplace=True)
        numeric_features = []
        categorical_features = []
        datetime_columns = []
        for column in dataset.columns:
            if column == resultantColumn:
                continue
            if dataset.dtypes[column] == np.int64 or dataset.dtypes[column] == np.float64:
                numeric_features.append(column)
            elif dataset.dtypes[column] == np.datetime64:
                datetime_columns.append(column)
            else:
                categorical_features.append(column)
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean'))
            ,('scaler', StandardScaler())
        ])
        numeric_transformer_without_scaling = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean'))
        ])
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent'))
            ,('encoder', OneHotEncoder(handle_unknown='ignore'))
        ])
        # datetime values can't be imputed so droping column if it has more than 10% null values otherwise dropping rows
        for column in datetime_columns:
            if 100.00*(dataset[column].isnull().sum()/dataset[column].sum()) >= 10:
                dataset.drop([column],axis = 1, inplace = True)
            else:
                dataset.drop(dataset[dataset[column] == np.NaN].index,inplace = True)
        
        preprocessor_with_scaling = ColumnTransformer(
            transformers=[
                ('numeric', numeric_transformer, numeric_features)
                ,('categorical', categorical_transformer, categorical_features)
            ])
        preprocessor_without_scaling = ColumnTransformer(
            transformers=[
                ('numeric', numeric_transformer_without_scaling, numeric_features)
                ,('categorical', categorical_transformer, categorical_features)
            ])
        noOfColumns = len(dataset.columns)
            
        featureExtractor = KernelPCA(n_components=noOfColumns-5)
        
        ridge_regression = Ridge()
        random_forest_regression = RandomForestRegressor()
        linear_svr = LinearSVR()
        linear_regression = LinearRegression()
        lasso_regression = Lasso()
        xgboost_regression = XGBRegressor()
        mlp_regression = MLPRegressor(max_iter=3000)
        ridge_pipeline = None
        randomForest_pipeline = None
        linear_svr_pipeline = None
        linear_regression_pipeline = None
        lasso_regression_pipeline = None
        xgboost_pipeline = None
        mlp_pipeline = None
        param_grid_ridge = {
            'RidgeRegression__alpha' : np.arange(0,1,0.03)
        }
        param_grid_lasso = {
            'LassoRegression__alpha' : np.arange(0,1,0.03)
        }
        param_grid_randomForest = {
            'RandomForestRegression__max_depth': [10, 20, 30, None],
            'RandomForestRegression__min_samples_split': [2, 5],
            'RandomForestRegression__n_estimators': [100,200, 500]
            }
        param_grid_linearSVR = {
                'Linear_SVR__C': [0.1, 0.5, 1.0, 10.0,0.01],
            }
        params_grid_xgboost= {
            'XGBoostRegression__gamma':[0.1,0.01,0.2,None],
            'XGBoostRegression__max_depth':[5,6,None],
            'XGBoostRegression__reg_alpha':[ 1e-2, 0.1,None]
        }
        params_grid_mlp = {
            'MLPRegression__hidden_layer_sizes': [(50,50), (100,50)],
            'MLPRegression__alpha': [0.0001,0.01, 0.05]
        }
        if noOfColumns > 100:
            ridge_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_with_scaling),
                ('FeatureExtraction',featureExtractor),
                ('RidgeRegression',ridge_regression)
            ])
            randomForest_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_without_scaling),
                ('FeatureExtraction',featureExtractor),
                ('RandomForestRegression',random_forest_regression)
            ])
            linear_svr_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_with_scaling),
                ('FeatureExtraction',featureExtractor),
                ('Linear_SVR',linear_svr)
            ])
            linear_regression_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_with_scaling),
                ('FeatureExtraction',featureExtractor),
                ('LinearRegression',linear_regression)
            ])
            lasso_regression_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_with_scaling),
                ('FeatureExtraction',featureExtractor),
                ('LassoRegression',lasso_regression)
            ])
            xgboost_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_without_scaling),
                ('FeatureExtraction',featureExtractor),
                ('XGBoostRegression',xgboost_regression)
            ])
            mlp_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_without_scaling),
                ('FeatureExtraction',featureExtractor),
                ('MLPRegression',mlp_regression)
            ])
        else:
            ridge_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_with_scaling),
                ('RidgeRegression',ridge_regression)
            ])
            randomForest_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_without_scaling),
                ('RandomForestRegression',random_forest_regression)
            ])
            linear_svr_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_with_scaling),
                ('Linear_SVR',linear_svr)
            ])
            linear_regression_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_with_scaling),
                ('LinearRegression',linear_regression)
            ])
            lasso_regression_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_with_scaling),
                ('LassoRegression',lasso_regression)
            ])
            xgboost_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_without_scaling),
                ('XGBoostRegression',xgboost_regression)
            ])
            mlp_pipeline = Pipeline(steps = [
                ('preprocessor',preprocessor_without_scaling),
                ('MLPRegression',mlp_regression)
            ])
        y = dataset[resultantColumn]
        X = dataset.drop(resultantColumn,axis=1)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # print(type(X_train))
        X_train, X_test, y_train, y_test = pd.DataFrame(X_train),pd.DataFrame(X_test),pd.DataFrame(y_train),pd.DataFrame(y_test)
        #testing ridge regression
        # ridge_pipeline.fit(X_train,y_train)
    
        ridge_cv = GridSearchCV(ridge_pipeline,param_grid=param_grid_ridge,scoring = 'explained_variance',n_jobs=-1)
        ridge_cv.fit(X_train,y_train)
        y_pred = ridge_cv.predict(X_test)
        ridge_expvar = explained_variance_score(y_test,y_pred)
        # ridge_expvar = ridge_cv.best_score_
        
        
        #testing random forest regression
        # randomForest_pipeline.fit(X_train,y_train)
        
        
        randomForest_cv = GridSearchCV(randomForest_pipeline,param_grid=param_grid_randomForest,scoring = 'explained_variance',n_jobs=-1)
        randomForest_cv.fit(X_train,y_train)
        y_pred = randomForest_cv.predict(X_test)
        randomForest_expvar = explained_variance_score(y_test,y_pred)

        # randomForest_expvar = randomForest_cv.best_score_
        # testing linear svr pipeline
        # linear_svr_pipeline.fit(X_train,y_train)

        linearSVR_cv = GridSearchCV(linear_svr_pipeline,param_grid=param_grid_linearSVR,scoring = 'explained_variance',n_jobs=-1)
        linearSVR_cv.fit(X_train,y_train)
        y_pred = linearSVR_cv.predict(X_test)
        linear_svr_expvar = explained_variance_score(y_test,y_pred)
        # linear_svr_expvar = linearSVR_cv.best_score_
        #testing linear regression
        linear_regression_pipeline.fit(X_train,y_train)
        y_pred = linear_regression_pipeline.predict(X_test)
        linear_regression_expvar = explained_variance_score(y_test,y_pred)
        #testing lasso regression
        # lasso_regression_pipeline.fit(X_train,y_train)

        lasso_cv = GridSearchCV(lasso_regression_pipeline,param_grid=param_grid_lasso,scoring = 'explained_variance',n_jobs=-1)
        lasso_cv.fit(X,y)
        y_pred = lasso_cv.predict(X_test)
        lasso_regression_expvar = explained_variance_score(y_test,y_pred)
        # lasso_regression_expvar = lasso_cv.best_score_

        #testing xgboost regression
        # xgboost_pipeline.fit(X_train,y_train)

        xgboost_cv = GridSearchCV(xgboost_pipeline,param_grid=params_grid_xgboost,scoring = 'explained_variance',n_jobs=-1)
        xgboost_cv.fit(X,y)
        y_pred = xgboost_cv.predict(X_test)
        xgboost_regression_expvar = explained_variance_score(y_test,y_pred)
        # xgboost_regression_expvar = xgboost_cv.best_score_

        #tesing mlp regressor
        # mlp_pipeline.fit(X_train,y_train)

        mlp_cv = GridSearchCV(mlp_pipeline,param_grid=params_grid_mlp,scoring = 'explained_variance',n_jobs=-1)
        mlp_cv.fit(X,y)
        y_pred = mlp_cv.predict(X_test)
        mlp_regression_expvar = explained_variance_score(y_test,y_pred)
        # mlp_regression_expvar = mlp_cv.best_score_

        results = {
            'Ridge' : ridge_expvar,
            'Random Forest' : randomForest_expvar,
            'Linear SVR' : linear_svr_expvar,
            'Linear Regression' : linear_regression_expvar,
            'Lasso Regression' : lasso_regression_expvar,
            'XGBRegressor' : xgboost_regression_expvar,
            "MLPRegressor" : mlp_regression_expvar 
        }
        results = pd.DataFrame(results,index=[resultantColumn])
        return results
