from numpy import log
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import multiprocessing

# Sklearn data analysis
import sklearn.metrics as sm
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from utils.aliases import DATASETS, OUT_DIR
from utils.file_handling import IMAGE_FORMAT


def prepare_sdg():
    df = pd.read_csv(DATASETS.get("sdg"))

    # The format of this file is weird, in the way, that it comes with two headers.
    # Where in the first row is the second header.
    # See file for 1st header

    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    return df


# Simplifying list comprehension
def _is_digit_and_is_between_range(column, min, max):
    if column.isdigit():
        if int(column) < min or int(column) > max:
            return True
    return False


def _move_down_header(df):
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    return df


def _create_plot(
    title,
    X_axis,
    y_axis,
    X_train,
    X_test,
    y_pred,
    coefficient,
    intercept,
    full_file_out_path,
    return_dict,
):
    # Create plot figure
    figure = plt.figure()

    # Define the axes
    ax = plt.axes()

    # Make scatterplot
    ax.scatter(X_axis, y_axis, edgecolor="k",
               facecolor="grey", label="Sample Data")

    # Add regression model to plot
    ax.plot(X_train, coefficient * X_train + intercept,
            label="Regression Model Prediction")

    # Add predicted regression model
    ax.plot(X_test, y_pred, label="Regression Model")

    # Defining plot labels and styling
    ax.set_title(title, fontsize=18)
    ax.set_xlabel("years", fontsize=14)
    ax.set_ylabel("suicide rate", fontsize=14)
    ax.legend(facecolor="white", fontsize=11)
    ax.axis("tight")

    # Add the figure to the return dict
    return_dict[title] = figure

    # Return figure (this does nothing when running it as a process, thats why we have the return_dict)
    return figure


def sdg_linear_regression(region, gender, preview, file_name=False):
    df = prepare_sdg()  # Prepare the dataset

    # Iterate through every value in the dataframe and remove split the data at every space (" "
    # E.g:  9.2 [4.2, 6.7] --> 9.2
    for index in df:
        column = df[index].str.split(" ").str[0]
        df.update(column)

    # Select row by region
    df = df[df["WHO region"] == region]
    # Transpose the dataframe
    df = df.T
    # Move down the dataframes header
    df = _move_down_header(df)
    # Reset the dataframes index
    df.reset_index(level=0, inplace=True)
    # Move down the dataframe's header again
    df = _move_down_header(df)

    # Iterate through every column value and change them to be lowercased
    df.columns = [x.lower() for x in df.columns]

    # After calling Transpose on the dataframe, the date column is defined as "sex" which is wrong, therefore we rename it back to "date"
    df = df.rename(columns={"sex": "date"})

    # Filter the current dataframe into a new dataframe with only the "date" column and specified gender colum
    # E.g. if "gender" is defined as "male", a dataframe with two rows: "date" and "male" is created
    data = [df["date"].astype(int), df[gender].astype(float)]
    headers = ["date", gender]
    df = pd.concat(data, axis=1, keys=headers)

    ### === Train Model === ###

    # Split the dataframe into independent X_axis and Y_axis
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

    coefficient = regressor.coef_
    intercept = regressor.intercept_

    # Predicted response vector
    y_pred = regressor.predict(X_test)

    # Output path for generated plot image
    full_file_out_path = f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}"

    manager = multiprocessing.Manager()

    # Return Dict (used to save the data we return from the plot process)
    return_dict = manager.dict()

    plot_title = f"sdg linear regression {region} {gender}"

    # Create multiprocess to generate plot
    create_plot_process = multiprocessing.Process(
        target=_create_plot,
        args=(
            plot_title,
            X_axis,
            y_axis,
            X_train,
            X_test,
            y_pred,
            coefficient,
            intercept,
            full_file_out_path,
            return_dict,
        ),
    )

    create_plot_process.start()
    # Join the plot process. This is usually only nessesary if we have multiple processes running,
    # however we want to make sure the function is finished before we proceed, therefore we add "join()"
    create_plot_process.join()

    # The finished plot - return_dict is an array of values, but we generate only one value, therefore we pick the one at index [0]
    finished_plot = return_dict.values()[0]

    if preview:
        finished_plot.savefig(full_file_out_path)
        return
    else:
        return mpld3.fig_to_html(finished_plot)
