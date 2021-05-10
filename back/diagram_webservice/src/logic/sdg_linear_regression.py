from utils.aliases import DATASETS, OUT_DIR
from utils.file_handling import IMAGE_FORMAT
from logic.basic import prepare_sdg

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import multiprocessing

# from numpy import log

import sklearn.metrics as sm  # Data analysis
from sklearn.preprocessing import StandardScaler  # Data analysis
from sklearn import linear_model  # Data analysis
from sklearn.linear_model import LinearRegression  # Data analysis
from sklearn.model_selection import train_test_split  # Data analysis


def _move_down_header(df):
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    return df


def _create_and_save_plot(
    title, X_axis, y_axis, X_train, X_test, y_pred, coefficient, intercept, full_file_out_path
):

    figure = plt.figure()
    ax = plt.axes()
    ax.scatter(X_axis, y_axis, edgecolor='k', facecolor='grey', label ="Sample Data")
    ax.plot(X_train, coefficient * X_train + intercept, label ="Regression Model")
    ax.plot(X_test, y_pred, label = "Regression Model Predicted")
    ax.set_title(title, fontsize=18)
    ax.set_xlabel("Suicide Rate", fontsize=14)
    ax.set_ylabel("Years", fontsize=14)
    ax.legend(facecolor='white', fontsize=11)
    ax.axis('tight')

    return figure


def sdg_linear_regression(region, gender, preview, file_name=False):

    print("################")
    print("################")
    print("################")
    print("################")
    print("################")

    df = prepare_sdg()  # Prepare the dataset

    # Iterate through every value in the dataframe and remove split the data at every space (" "
    # E.g:  9.2 [4.2, 6.7] --> 9.2
    for index in df:
        column = df[index].str.split(" ").str[0]
        df.update(column)

    df = df[df["WHO region"] == region]  # Select row by region
    df = df.T  # Transpose the dataframe
    df = _move_down_header(df)  # Move down the dataframes header
    df.reset_index(level=0, inplace=True)  # Reset the dataframes index
    df = _move_down_header(df)  # Move down the dataframe's header again

    df.columns = [
        x.lower() for x in df.columns
    ]  # Iterate through every column value and change them to be lowercased
    df = df.rename(columns={"sex": "date"})  # Rename "sex" column value to be "date"

    data = [df["date"].astype(int), df[gender].astype(float)]
    headers = ["date", gender]
    df = pd.concat(data, axis=1, keys=headers)

    # Train Model
    # Split data into independent X_axis and Y_axis
    # X_axis = df["date"].values.reshape(-1,1) # Define X_axis values and reshape the data
    # y_axis = df["both"].values.reshape(-1,1) # Define X_axis values and reshape the data

    X_axis = df.iloc[:, :-1].values

    y_axis = df.iloc[:, 1].values

    # Shaping the subsets
    X_train, X_test, y_train, y_test = train_test_split(
        X_axis, y_axis, test_size=0.33, random_state=0
    )

    # Create an instance of a Linear Regression Model
    regressor = LinearRegression().fit(
        X_train, y_train
    )  # Fit the X_train and y_train into the regressor model

    # Regression coefficient
    coefficient = regressor.coef_
    # Regression intercept
    intercept = regressor.intercept_

    # Predicted response vector
    y_pred = regressor.predict(X_test)

    full_file_out_path = f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}"
    fig = _create_and_save_plot("Linear Regression",
            X_axis,
            y_axis,
            X_train,
            X_test,
            y_pred,
            coefficient,
            intercept,
            full_file_out_path)

    if preview:
        fig.savefig(full_file_out_path)
        return
    else:
        return mpld3.fig_to_html(fig)
