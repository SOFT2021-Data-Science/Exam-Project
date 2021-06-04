from numpy import log
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import multiprocessing

# Sklearn data analysis
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans

from utils.aliases import DATASETS, OUT_DIR
from utils.file_handling import IMAGE_FORMAT


def prepare_sdg(region, gender):
    df = pd.read_csv(DATASETS.get("sdg"))

    # The format of this file is weird, in the way, that it comes with two headers.
    # Where in the first row is the second header.
    # See file for 1st header

    header = df.iloc[0]
    df = df[1:]
    df.columns = header

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
    return df


def sdg_get_list_of_all_values_in_row_by_column_name(column_name):
    """Function to return a list of all values in a row for the sdg dataset

    :param column_name: Used to filter the column by the specified column name
    :type column_name: String
    :return: Returns a list of all values in a row
    :rtype: pandas.series.tolist
    """    
    column_name = column_name.lower()
    df = pd.read_csv(DATASETS.get("sdg"))

    # The format of this file is weird, in the way, that it comes with two headers.
    # Where in the first row is the second header.
    # See file for 1st header

    header = df.iloc[0]
    df = df[1:]
    df.columns = header

    # Iterate through every value in the dataframe and remove split the data at every space (" "
    # E.g:  9.2 [4.2, 6.7] --> 9.2
    for index in df:
        column = df[index].str.split(" ").str[0]
        df.update(column)

    df.columns = [x.lower() for x in df.columns]
    df = df.groupby(column_name, as_index=False).sum()

    return df[column_name].values.tolist()


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


# WCSS is the sum of squared distance between each point and the centroid in a cluster
def _make_wcss(min, max, X):
    """WCSS is the sum of squared distance between each point and the centroid in a cluster

    :param min: The minimum number of clusters
    :type min: Integer
    :param max: The maximum number of clusters
    :type max: Integer
    :param X: The values of our dataframe
    :type X: Pandas.DataFrame.values
    :return: Returns a list of the generated distortions
    :rtype: List
    """

    # The number of clusters we want on the pot (this can not be larger than our X value)
    K = range(min, max)

    # To get the values used in the graph, we train multiple models using a different number of clusters and storing the value of the "intertia_" property (distortions) eevery time
    distortions = []

    # For each value in K, create a new kmeans model and train it with the value of k
    for k in K:
        model = KMeans(n_clusters=k)
        model.fit(X)
        distortions.append(model.inertia_)
    return distortions


def _create_linear_regression_plot(
    title,
    X_axis,
    y_axis,
    X_train,
    X_test,
    y_pred,
    coefficient,
    intercept,
    return_dict,
):
    """Function to generate a linear regression plot

    :param title: The title of the plot
    :type title: String
    :param X_axis: The X axis values for the plot
    :type X_axis: numpy.ndarray
    :param y_axis: The Y axis values for the plot
    :type y_axis: numpy.ndarray
    :param X_train: Trained values for X]
    :type X_train: numpy.ndarray
    :param X_test: Test values for X
    :type X_test: numpy.ndarray
    :param y_pred: Predicted regression model
    :type y_pred: numpy.ndarray
    :param coefficient: The coefficient is used in the regressor model
    :type coefficient: numpy.ndarray
    :param intercept: The intercept is used in the regressor model
    :type intercept: numpy.ndarray
    :param return_dict: A shared list object that is used to save data to from inside a multiprocess
    :type return_dict: multiprocessing.managers.DictProxy
    :return: Returns the generated figure
    :rtype: matplotlib.figure.Figure
    """

    # Create plot figure
    figure = plt.figure()

    # Define the axes
    ax = plt.axes()

    # Make scatterplot
    ax.scatter(X_axis, y_axis, edgecolor="k", facecolor="grey", label="Sample Data")

    # Add regression model to plot
    ax.plot(
        X_train, coefficient * X_train + intercept, label="Regression Model Prediction"
    )

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


def _create_kmeans_cluster_plot(title, X, kmeans, return_dict):
    """Function to generate scatterplot for k-means clustering

    :param title: The title of the scatterplot
    :type title: String
    :param X: Suicide data values
    :type X: Pandas.DataFrame.values
    :param kmeans: Kmeans
    :type kmeans: sklearn.cluster._kmeans.KMeans
    :param return_dict: A shared list object that is used to save data to from inside a multiprocess
    :type return_dict: multiprocessing.managers.DictProxy
    :return: Returns the generated figure
    :rtype: matplotlib.figure.Figure
    """
    # Create plot figure
    figure = plt.figure()
    # Define the axes
    ax = plt.axes()
    # Get the center position of each cluster
    centroids = kmeans.cluster_centers_
    # Plot the data into a scatter plot
    ax.scatter(X[:, 0], X[:, 1], c=kmeans.labels_.astype(float), s=100, alpha=0.5)
    ax.scatter(
        centroids[:, 0],
        centroids[:, 1],
        edgecolor="k",
        facecolor="red",
        s=50,
        alpha=0.75,
    )
    ax.set_title(title, fontsize=18)
    ax.set_xlabel("years", fontsize=14)
    ax.set_ylabel("suicide rate", fontsize=14)
    ax.axis("tight")
    # Add the figure to the return dict
    return_dict[title] = figure
    # Return figure (this does nothing when running it as a process, thats why we have the return_dict)
    return figure


def _create_kmeans_elbow_plot(min, max, wcss, title, return_dict):
    """Function to generate elbow plot for optimal K

    :param min: The maximum Y value
    :type min: Integer
    :param max: The maximum X value
    :type max: Integer
    :param wcss: The WCSS list of distortions
    :type wcss: List
    :param title: The title of the plot
    :type title: String
    :param return_dict: A shared list object that is used to save data to from inside a multiprocess
    :type return_dict: multiprocessing.managers.DictProxy
    :return: [description]
    :rtype: [type]
    """

    # Create plot figure
    figure = plt.figure()
    # Define the axes
    ax = plt.axes()

    # Get the center position of each cluster
    ax.set_title(title, fontsize=18)
    ax.set_xlabel("clusters", fontsize=14)
    ax.set_ylabel("WCSS", fontsize=14)
    ax.plot(range(min, max), wcss, marker="o")
    ax.axis("tight")

    # Add the figure to the return dict
    return_dict[title] = figure
    # Return figure (this does nothing when running it as a process, thats why we have the return_dict)
    return figure

def _create_polynomial_regression_plot(title, r2_score, degrees, future_years, x_test, y_test, x_train, y_train, x_predicted, y_predicted, regression_line, return_dict):
    """Function to generate polynomial regression pot for the sdg dataset

    :param title: The title of the plot
    :type title: String
    :param r2_score: The calculated r2 score for the regression model
    :type r2_score: Float
    :param degrees: The amount of degrees in the regression model
    :type degrees: Integer
    :param future_years: The amount of years that is used in the future prediction
    :type future_years: Integer
    :param x_test: Test data on the x_axis for the regression model
    :type x_test: numpy.ndarray
    :param y_test: The test data on the y_axis for the regression model
    :type y_test: numpy.ndarray
    :param x_train: The train data on the x_axis for the regression model
    :type x_train: numpy.ndarray
    :param y_train: The train data on the y_axis for the regression model
    :type y_train: numpy.ndarray
    :param x_predicted: The predicted data on the x_axis for the regression model
    :type x_predicted: numpy.ndarray
    :param y_predicted: The predicted data on the y_axis for the regression model
    :type y_predicted: numpy.ndarray
    :param regression_line: The regression line for the regression model
    :type regression_line: numpy.ndarray
    :param return_dict: A shared list object that is used to save data to from inside a multiprocess
    :type return_dict: multiprocessing.managers.DictProxy
    :return: Returns the generated figure
    :rtype: matplotlib.figure.Figure
    """   
    
    # Create plot figure
    figure = plt.figure(figsize=(10,6))

    # Round r2_score to make it more readable
    r2_score = round(r2_score, 4)
    # Define the axes
    ax = plt.axes()
    ax.plot([], [], ' ', label="R2 SCORE: " + str(r2_score))
    ax.plot([], [], ' ', label="Degrees: " + str(degrees))
    ax.plot([], [], ' ', label="Years Predicted: " + str(future_years))

    # Make scatterplot of actual data
    ax.scatter(x_test, y_test, c="orange", label="Testing Data")
    ax.scatter(x_train, y_train, c="red", label="Training Data")

    # Make scatterplot of predicted data
    ax.scatter(x_predicted, y_predicted, c='blue', label='Predicted Future Value')

    # Add regression model to plot
    ax.plot(x_train, regression_line, c='black', label='Polynomial regression line')    

    # Defining plot labels and styling
    ax.set_title(title, fontsize=18)
    ax.set_xlabel("years", fontsize=14)
    ax.set_ylabel("suicide rate", fontsize=14)
    ax.legend(facecolor="white", fontsize=11, loc="upper left")
    ax.axis("tight")

    # Add the figure to the return dict
    return_dict[title] = figure

    # Return figure (this does nothing when running it as a process, thats why we have the return_dict)
    return figure


def _create_plot_for_two_genders_by_region(title, male_x_1, male_y_1, female_x_1, female_y_1, return_dict):
    """Function to generate plot for male and female data in a region for the sdg dataset

    :param title: The title of the plot
    :type title: String
    :param male_x_1: The males x_axis value for the plot
    :type male_x_1: numpy.ndarray
    :param male_y_1: The males y_axis value for the plot
    :type male_y_1: numpy.ndarray
    :param female_x_1: The females x_axis value for the plot
    :type female_x_1: numpy.ndarray
    :param female_y_1: The females y_axis value for the plot
    :type female_y_1: numpy.ndarray
    :param return_dict: A shared list object that is used to save data to from inside a multiprocess
    :type return_dict: multiprocessing.managers.DictProxy
    :return: Returns the generated figure
    :rtype: matplotlib.figure.Figure
    """   

    # Create plot figure
    figure = plt.figure(figsize=(10,6))

    # Define the axes
    ax = plt.axes()

    # Make scatterplot of actual data
    ax.plot(male_x_1, male_y_1, c="orange", label="Male")
    ax.plot(female_x_1, female_y_1, c="red", label="Female")

    # Defining plot labels and styling
    ax.set_title(title, fontsize=18)
    ax.set_xlabel("years", fontsize=14)
    ax.set_ylabel("suicide rate pr 100k population", fontsize=14)
    ax.legend(facecolor="white", fontsize=11, loc="upper left")
    ax.axis("tight")
    # Add the figure to the return dict
    return_dict[title] = figure
    return figure
    
def _create_plot_for_gender_for_two_regions(title, first_region_name, second_region_name, gender, first_region_x, first_region_y, second_region_x, second_region_y , return_dict):
    """Function to generate plot for specified gender between two countries for the sdg dataset 

    :param title: Title of the plot
    :type title: String
    :param first_country_name: The name of the first country to show on the plot
    :type first_country_name: String
    :param second_country_name: The name of the second country to show on the plot
    :type second_country_name: String
    :param gender: The specified gender for the data
    :type gender: String
    :param first_country_x: The first countries x_axis value for the plot
    :type first_country_x: np.ndarray
    :param first_country_y: The first countries y_axis value for the plot
    :type first_country_y: np.ndarray
    :param second_country_x: The second countries x_axis value for the plot
    :type second_country_x: np.ndarray
    :param second_country_y: The second countries y_axis value for the plot
    :type second_country_y: np.ndarray
    :param return_dict: A shared list object that is used to save data to from inside a multiprocess
    :type return_dict: multiprocessing.managers.DictProxy
    :return: Returns the generated figure
    :rtype: matplotlib.figure.Figure
    """    
    
    # Create plot figure
    figure = plt.figure(figsize=(10,6))

    # Define the axes
    ax = plt.axes()

    # Make scatterplot of actual data
    ax.plot(first_region_x, first_region_y, c="orange", label=first_region_name)
    ax.plot(second_region_x, second_region_y, c="red", label=second_region_name)

    # Defining plot labels and styling
    ax.set_title(title, fontsize=12)
    ax.set_xlabel("years", fontsize=14)
    ax.set_ylabel("suicide rate pr 100k population", fontsize=14)
    ax.legend(facecolor="white", fontsize=11, loc="upper left")
    ax.axis("tight")
    # Add the figure to the return dict
    return_dict[title] = figure
    return figure

def sdg_linear_regression(region, gender, preview, file_name=False):
    """Function to generate linear regression model for the sdg dataset

    :param region: Used to filter the dataset by region
    :type region: String
    :param gender: Used to filter the dataset by gender
    :type gender: String
    :param preview: Boolean value used to determent if the return value is 'Preview' or 'Template' based on True or False
    :type preview: Boolean
    :param file_name: Used to generate the plots filename . Defaults to False.
    :type file_name: Boolean, Optional
    :return: If preview is FALSE, then we return a mpld3-figure as html, and if it's true it returns nothing
    :rtype: mpld3.fig_to_html
    """

    # Prepare the dataset
    df = prepare_sdg(region, gender)

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
        target=_create_linear_regression_plot,
        args=(
            plot_title,
            X_axis,
            y_axis,
            X_train,
            X_test,
            y_pred,
            coefficient,
            intercept,
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


def sdg_kmeans_cluster(region, gender, clusters, preview, file_name=False):
    """Function to generate k-means elbow method for the sdg dataset

    :param region: Used to filter the dataset by region
    :type region: String
    :param gender: Used to filter the dataset by gender
    :type gender: String
    :param clusters: Used to define the number of clusters
    :type clusters: Integer
    :param preview: Boolean value used to determent if the return value is 'Preview' or 'Template' based on True or False
    :type preview: Boolean
    :param file_name: Used to generate the plots filename . Defaults to False.
    :type file_name: Boolean, Optional
    :return: If preview is FALSE, then we return a mpld3-figure as html, and if it's true it returns nothing
    :rtype: mpld3.fig_to_html
    """

    # Prepare the dataset
    df = prepare_sdg(region, gender)

    # Generate Kmeans
    kmeans = KMeans(init="k-means++", n_clusters=clusters, n_init=3, random_state=10)

    # The values of the dataframe
    X = df.values

    # Train the kmeans model with our X values
    kmeans.fit(X)

    manager = multiprocessing.Manager()

    # Return Dict (used to save the data we return from the plot process)
    return_dict = manager.dict()

    # The title of the plot
    plot_title = f"sdg Cluster k-means {region} {gender}"

    # Create multiprocess to generate plot
    create_plot_process = multiprocessing.Process(
        target=_create_kmeans_cluster_plot,
        args=(
            plot_title,
            X,
            kmeans,
            return_dict,
        ),
    )

    create_plot_process.start()
    # Join the plot process. This is usually only nessesary if we have multiple processes running,
    # however we want to make sure the function is finished before we proceed, therefore we add "join()"
    create_plot_process.join()

    # The finished plot - return_dict is an array of values, but we generate only one value, therefore we pick the one at index [0]
    finished_plot = return_dict.values()[0]

    # Output path for generated plot image
    full_file_out_path = f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}"

    if preview:
        finished_plot.savefig(full_file_out_path)
        return
    else:
        return mpld3.fig_to_html(finished_plot)


def sdg_kmeans_elbow(region, gender, clusters, preview, file_name=False):
    """Function to generate k-means elbow method for the sdg dataset

    :param region: Used to filter the dataset by region
    :type region: String
    :param gender: Used to filter the dataset by gender
    :type gender: String
    :param clusters: Used to define the number of clusters in the WCSS model
    :type clusters: Interger
    :param preview: Boolean value used to determent if the return value is 'Preview' or 'Template' based on True or False
    :type preview: Boolean
    :param file_name: Used to generate the plots filename . Defaults to False.
    :type file_name: Boolean, Optional
    :return: If preview is FALSE, then we return a mpld3-figure as html, and if it's true it returns nothing
    :rtype: mpld3.fig_to_html
    """

    # Prepare the data
    df = prepare_sdg(region, gender)

    # The values of the dataframe
    X = df.values

    # Minimum point on WCSS
    min = 1

    # Max point on WCSS (we plus this with the minimum value, so that the input value matches the points shown on the plot)
    # E.g: If we insert 5 without addding the minimum value, the plot would only show 4 plots, since the range between 1 and 5 is 4
    max = clusters + min

    # WCSS is the sum of squared distance between each point and the centroid in a cluster
    # This is used to generate the "legs"/"points" on the plot
    WCSS = _make_wcss(min, max, X)

    manager = multiprocessing.Manager()

    # Return Dict (used to save the data we return from the plot process)
    return_dict = manager.dict()

    # The title of the plot
    plot_title = f"sdg k-means elbow {region} {gender}"

    # Create multiprocess to generate plot
    create_plot_process = multiprocessing.Process(
        target=_create_kmeans_elbow_plot,
        args=(
            min,
            max,
            WCSS,
            plot_title,
            return_dict,
        ),
    )

    create_plot_process.start()
    # Join the plot process. This is usually only nessesary if we have multiple processes running,
    # however we want to make sure the function is finished before we proceed, therefore we add "join()"
    create_plot_process.join()

    # The finished plot - return_dict is an array of values, but we generate only one value, therefore we pick the one at index [0]
    finished_plot = return_dict.values()[0]

    # Output path for generated plot image
    full_file_out_path = f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}"

    if preview:
        finished_plot.savefig(full_file_out_path)
        return
    else:
        return mpld3.fig_to_html(finished_plot)



def sdg_polynomial_regression(region, gender, degrees, future_years, preview, file_name=False):
    """Function to generate polynomial regression method and future prediction for the sdg dataset

    :param region: Used to filter the dataset by region
    :type region: String
    :param gender: Used to filter the dataset by gender
    :type gender: String
    :param degrees: Used to define the number of degrees in regression model
    :type degrees: Interger
    :param future_years: Used to define the number of future years to predict
    :type future_years: Integer
    :param preview: Boolean value used to determent if the return value is 'Preview' or 'Template' based on True or False
    :type preview: Boolean
    :param file_name: Used to generate the plots filename . Defaults to False.
    :type file_name: Boolean, Optional
    :return: If preview is FALSE, then we return a mpld3-figure as html, and if it's true it returns nothing
    :rtype: mpld3.fig_to_html
    """
    # Prepare the dataset
    df = prepare_sdg(region, gender)

    # Reverse the dataframe
    df = df.iloc[::-1]

    # Split the dataframe into independent X_axis and Y_axis
    x = df.iloc[:, :-1].values
    y = df.iloc[:, 1].values

    # Create train and test subset data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Reshape the data
    x_train = x_train.reshape(-1, 1)
    y_train = y_train.reshape(-1, 1)

    # Sort the data
    y_train = y_train[x_train[:,0].argsort()]
    x_train = x_train[x_train[:, 0].argsort()]

    # Fit the X_train and into the regressor model
    poly = PolynomialFeatures(degree=degrees)
    x_poly = poly.fit_transform(x_train)

    # Fit x_poly and y_train into the regressor model
    poly_reg = LinearRegression()
    poly_reg.fit(x_poly, y_train)

    # Calculate the r2_score for the model
    # The closer the r2_score is to 1 the more precise our predictions will be.
    r2_score = poly_reg.score(x_poly, y_train)

    # Create the regression line
    regression_line = poly_reg.predict(x_poly)


    # Dataframe for future predictions
    df_future_predictions = pd.DataFrame(columns = df.columns)

    for i in range(future_years):
        i+=1
        year = x[len(x)-1] + i

        # Predict suicide rate for specified year.
        # E.g. "poly.fit_transform([2020])" will a suicide rate for the year 2020
        suicides_no = poly_reg.predict(poly.fit_transform([year]))
        ob = {df.columns[0]:int(year[0]), df.columns[1]: suicides_no[0]}
        df_future_predictions = df_future_predictions.append(ob, ignore_index=True)

    # X and Y coordinates for the predicted future values
    x_new_predicted = df_future_predictions.iloc[:, :-1].values
    y_new_predicted = df_future_predictions.iloc[:,1].values

    # Output path for generated plot image
    full_file_out_path = f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}"

    manager = multiprocessing.Manager()

    # Return Dict (used to save the data we return from the plot process)
    return_dict = manager.dict()

    plot_title = f"sdg polynomial regression {region} {gender}"

    # Create multiprocess to generate plot
    create_plot_process = multiprocessing.Process(
        target=_create_polynomial_regression_plot,
        args=(plot_title, r2_score, degrees, future_years, x_test, y_test, x_train, y_train, x_new_predicted, y_new_predicted, regression_line, return_dict),
    )

    create_plot_process.start()
    # Join the plot process. This is usually only necessary if we have multiple processes running,
    # however we want to make sure the function is finished before we proceed, therefore we add "join()"
    create_plot_process.join()

    # The finished plot - return_dict is an array of values, but we generate only one value, therefore we pick the one at index [0]
    finished_plot = return_dict.values()[0]

    if preview:
        finished_plot.savefig(full_file_out_path)
        return
    else:
        return mpld3.fig_to_html(finished_plot)

def sdg_compare_male_female_from_region(region, preview, file_name=False):
    """Function to compare male and female suicide rates in a region for the sdg dataset

    :param region: Used to filter the dataset by region
    :type region: String
    :param preview: Boolean value used to determent if the return value is 'Preview' or 'Template' based on True or False
    :type preview: Boolean
    :param file_name: Used to generate the plots filename . Defaults to False.
    :type file_name: Boolean, Optional
    :return: If preview is FALSE, then we return a mpld3-figure as html, and if it's true it returns nothing
    :rtype: mpld3.fig_to_html
    """    
    
    # Retrieve sdg dataset for two regions
    female_df = prepare_sdg(region, "female")
    male_df = prepare_sdg(region, "male")

    # Split the region data into two different X and Y coordinates
    maleX = male_df.iloc[:, :-1].values
    maleY = male_df.iloc[:,1].values
    femaleX = female_df.iloc[:, :-1].values
    femaleY = female_df.iloc[:,1].values

    # Output path for generated plot image
    full_file_out_path = f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}"

    manager = multiprocessing.Manager()

    # Return Dict (used to save the data we return from the plot process)
    return_dict = manager.dict()

    plot_title = f"Comparing male and female suicide rate for {region} pr 100k population"

    # Create multiprocess to generate plot
    create_plot_process = multiprocessing.Process(
        target=_create_plot_for_two_genders_by_region,
        args=(plot_title, maleX, maleY, femaleX, femaleY, return_dict),
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

        
def sdg_compare_suicide_rates_for_gender_between_two_regions(first_region, second_region, gender, preview, file_name=False):
    """Function to compare suicide rates for a specified gender between two regions for the sdg dataset

    :param first_region: Used to filter dataset by the first region specified
    :type first_region: String
    :param second_region: Used to filter dataset by the second region specified
    :type second_region: String
    :param gender: Used to filter dataset by gender
    :type gender: String
    :param preview: Boolean value used to determent if the return value is 'Preview' or 'Template' based on True or False
    :type preview: Boolean
    :param file_name: Used to generate the plots filename . Defaults to False.
    :type file_name: Boolean, Optional
    :return: If preview is FALSE, then we return a mpld3-figure as html, and if it's true it returns nothing
    :rtype: mpld3.fig_to_html
    """  

    # Retrieve sdg dataset for two regions
    region_1 = prepare_sdg(first_region, gender)
    region_2 = prepare_sdg(second_region, gender)

    # Split the region data into two different X and Y coordinates
    first_region_x = region_1.iloc[:, :-1].values
    first_region_y = region_1.iloc[:,1].values
    second_region_x = region_2.iloc[:, :-1].values
    second_region_y = region_2.iloc[:,1].values


    # Output path for generated plot image
    full_file_out_path = f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}"

    manager = multiprocessing.Manager()

    # Return Dict (used to save the data we return from the plot process)
    return_dict = manager.dict()

    plot_title = f"Comparing {gender} suicide rate pr 100k population between {first_region} and {second_region}"

    # Create multiprocess to generate plot
    create_plot_process = multiprocessing.Process(
        target=_create_plot_for_gender_for_two_regions,
        args=(plot_title, first_region, second_region, gender, first_region_x, first_region_y, second_region_x, second_region_y , return_dict),
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



