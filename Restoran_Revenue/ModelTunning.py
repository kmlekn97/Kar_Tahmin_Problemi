import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

from GridSearchCVParametars import GridSearchCVParametars


class ModelTunning():
    __X_train=None
    __X_test = None
    __y_train = None
    __y_test = None
    __X_train_scaller=None
    __X_test_scaller=None
    __revenue=[]
    __errors=[]
    def ArrayToplam(self,np):
        dp=pd.Series(np)
        return dp.sum()
    def CraateDataset(self,X,y):
        self.__X_train, self.__X_test, self.__y_train, self.__y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        scaler = StandardScaler()
        scaler.fit(self.__X_train)
        self.__X_train_scaller = scaler.transform(self.__X_train)
        self.__X_test_scaller = scaler.transform(self.__X_test)
    def CreateModel(self,model):
        modelfit = model.fit(self.__X_train_scaller, self.__y_train)
        return modelfit
    def model(self,model_fit,model_params):
        grid_model = GridSearchCV(model_fit, model_params, cv=2)
        grid_model.fit(self.__X_train_scaller, self.__y_train)
        return grid_model
    def ModelSolve(self,model_fit,model_params,classification):
        grid_model = self.model(model_fit,model_params)
        self.model_fit = classification.fit(self.__X_train_scaller, self.__y_train)
        y_pred = classification.predict(self.__X_test_scaller)
        self.__revenue=self.ArrayToplam(y_pred)
        print(y_pred)
        print(accuracy_score(self.__y_test, y_pred))
        print(np.sqrt(mean_squared_error(self.__y_test, y_pred)))
        self.__errors.append(np.sqrt(mean_squared_error(self.__y_test, y_pred)))
    def RandomForest(self,params):
        rf_model = RandomForestRegressor(random_state=42)
        rf_model.fit(self.__X_train, self.__y_train)
        rf_params = params
        rf_cv_model = GridSearchCV(rf_model,
                                   rf_params,
                                   cv=10,
                                   n_jobs=-1)
        rf_cv_model.fit(self.__X_train, self.__y_train)
        rf_tuned = RandomForestRegressor(max_depth=rf_cv_model.best_params_['max_depth'],
                                         max_features=rf_cv_model.best_params_['max_features'],
                                         n_estimators=rf_cv_model.best_params_['n_estimators'])
        rf_tuned.fit(self.__X_train, self.__y_train)
        y_pred = rf_tuned.predict(self.__X_test)
        self.__revenue=self.ArrayToplam(y_pred)
        print(y_pred)
        print(np.sqrt(mean_squared_error(self.__y_test, y_pred)))
        self.__errors.append(np.sqrt(mean_squared_error(self.__y_test, y_pred)))


    def SolveGB(self,model,params):
        model.fit(self.__X_train, self.__y_train)
        solve_params = params
        type_cv_model = GridSearchCV(model, solve_params, cv=10, n_jobs=-1, verbose=2)
        type_cv_model.fit(self.__X_train, self.__y_train)
        type_tuned = GradientBoostingRegressor(learning_rate=type_cv_model.best_params_['learning_rate'],
                                              max_depth=type_cv_model.best_params_['max_depth'],
                                              n_estimators=type_cv_model.best_params_['n_estimators'],
                                              subsample=type_cv_model.best_params_['subsample'])

        type_tuned = type_tuned.fit(self.__X_train, self.__y_train)
        y_pred = type_tuned.predict(self.__X_test)
        self.__revenue=self.ArrayToplam(y_pred)
        print(y_pred)
        print(np.sqrt(mean_squared_error(self.__y_test, y_pred)))
        self.__errors.append(np.sqrt(mean_squared_error(self.__y_test, y_pred)))
    def minerrors(self):
        data = self.__errors[0]
        indis = 0
        for i in range(len(self.__errors)):
            if self.__errors[i] < data:
                data = self.__errors[i]
                indis = i
        return indis
    def SolveOptimalMethod(self,X,y,gParamaters):
        error=self.minerrors()
        print(error)
        if error==0:
            mlpc = MLPClassifier()
            self.CraateDataset(X, y)
            self.CreateModel(mlpc)
            gParamaters = GridSearchCVParametars()
            classifacation = gParamaters.Paramaters(self, mlpc, MLPClassifier)
            self.ModelSolve(self.CreateModel(mlpc), classifacation[1], classifacation[0])
        elif error==1:
            self.RandomForest(gParamaters.RF())
        elif error==2:
            GBM=GradientBoostingRegressor()
            self.SolveGB(GBM,gParamaters.GB())
        elif error==3:
            XGB=XGBRegressor()
            self.SolveGB(XGB,gParamaters.GB())
        elif error == 4:
            lightgbm=LGBMRegressor()
            self.SolveGB(lightgbm, gParamaters.GB())
        else:
            catb=CatBoostRegressor()
            self.SolveGB(catb,gParamaters.GB())
    def displayRevenue(self):
        print(self.__revenue)
    def Revenue(self):
        return self.__revenue