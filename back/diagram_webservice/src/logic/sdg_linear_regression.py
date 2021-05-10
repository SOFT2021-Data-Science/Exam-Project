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
    title, X_axis, y_axis, X_train, X_test, y_pred, regressor, full_file_out_path
):
    # Regression coe
    a = regressor.coef_
    b = regressor.intercept_

    plt.title(title)
    plt.scatter(X_axis, y_axis, color="green")
    plt.plot(X_train, a * X_train + b, color="blue")
    plt.plot(X_test, y_pred, color="orange")
    plt.xlabel("Hours")
    plt.ylabel("Scores")

    plt.savefig(full_file_out_path)



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

    # Regression coe
    a = regressor.coef_
    b = regressor.intercept_

    # Predicted response vector
    y_pred = regressor.predict(X_test)

    # fig = plt.figure()

    # full_file_out_path = f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}"
    # plt.savefig(full_file_out_path)

    # fig = plt.figure()
    # plt.title('Linear Regression')
    # ax = fig.add_axes([0,0,1,1])
    # ax.scatter(X_axis, y_axis, color='green')
    # ax.plot(X_train, a*X_train + b, color='blue')
    # ax.plot(X_test, y_pred, color='orange')
    # ax.set_xlabel('Years')
    # ax.set_ylabel('Suicide Rate')
    # ax.set_title(f"Linear Regression {region} {gender}")

    if preview:
        full_file_out_path = f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}"
        p = multiprocessing.Process(
            target=_create_and_save_plot,
            args=(
                "Linear Regression",
                X_axis,
                y_axis,
                X_train,
                X_test,
                y_pred,
                regressor,
                full_file_out_path,
            ),
        )
        p.start()
        p.join()
        return
    else:
        # p = multiprocessing.Process(target=_create_and_save_plot, args=("Linear Regression", X_axis, y_axis, X_train, X_test, y_pred, regressor, full_file_out_path))
        # p.start()
        # p.join()
        return mpld3.fig_to_html(plt)
