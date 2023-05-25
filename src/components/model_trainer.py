#train different models and evaluate
import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path:str = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array): #the arguments are the output of data transformation
        try:
            logging.info("Split training and test input data")
            #the data fed in has target value at the last column of the data(arr)
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            #model dictionary
            models = {
                'Linear Regression' : LinearRegression(),
                'K-Neighbors Regressor' : KNeighborsRegressor(),
                'Decision Tree' : DecisionTreeRegressor(),
                'Random Forest Regressor' : RandomForestRegressor(),
                'XGBRegressor' : XGBRegressor(),
                'AdaBoost Regressor' : AdaBoostRegressor(),
                'Gradient Boosting' : GradientBoostingRegressor(),
            }

            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train,
                                                X_test=X_test, y_test=y_test, models=models)
            
            #pick the best model
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            #pick the best model score
            best_model_score = max(model_report.values())

            #set the threshold
            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logging.info("Best model found!")

            #save the model
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            return f"Best model : {best_model_name}, The score : {r2_square}"

        except Exception as e:
            raise CustomException(e,sys)
