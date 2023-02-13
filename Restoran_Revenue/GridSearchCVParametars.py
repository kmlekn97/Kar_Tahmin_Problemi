class GridSearchCVParametars():
    def Paramaters(self,mTunning,model,type):
        mlpc_params = {
            'alpha': [0.1, 0.01, 0.02, 0.005],
            'hidden_layer_sizes': [(4, 4), (8, 8), (16, 16)],
            'activation': ['relu', 'logistic', 'tanh', 'sigmoid', 'leaky relu', 'parametric relu', 'softmax', 'relu6',
                           'binary step', 'identity', 'swish', 'hard swish']
        }
        grid_model = mTunning.model(mTunning.CreateModel(model), mlpc_params)
        classifacation = type(activation=grid_model.best_params_['activation'],
                                       alpha=grid_model.best_params_['alpha'],
                                       hidden_layer_sizes=grid_model.best_params_['hidden_layer_sizes'])
        return classifacation,mlpc_params

    def RF(self):
        rf_params = {'max_depth': list(range(1, 10)),
                     'max_features': [4, 8, 16],
                     'n_estimators': [16, 8]}
        return rf_params
    def GB(self):
        solve_params = {
            'learning_rate': [0.001, 0.01, 0.1, 0.2],
            'max_depth': [4, 8, 16],
            'n_estimators': [16, 8],
            'subsample': [1, 0.5, ],
        }
        return solve_params