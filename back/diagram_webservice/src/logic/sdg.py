from numpy import log
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import multiprocessing

# Sklearn data analysis
from sklearn.linear_model import LinearRegression
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
    ax.plot(X_train, coefficient * X_train + intercept, label="Regression Model Prediction")

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

def _create_kmeans_cluster_plot(
    title,
    X,
    kmeans,
    return_dict
):
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
    centroids =kmeans.cluster_centers_
    # Plot the data into a scatter plot
    ax.scatter(X[:,0],X[:,1],c=kmeans.labels_.astype(float),s=100,alpha=0.5)
    ax.scatter(centroids[:,0],centroids[:,1], edgecolor="k", facecolor="red", s=50, alpha=0.75)
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
    ax.plot(range(min, max), wcss, marker='o')
    ax.axis("tight")

    # Add the figure to the return dict
    return_dict[title] = figure
    # Return figure (this does nothing when running it as a process, thats why we have the return_dict)
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
    df=prepare_sdg(region, gender)

    # Generate Kmeans 
    kmeans = KMeans(init='k-means++',n_clusters=clusters,n_init=3, random_state = 10)

    # The values of the dataframe
    X=df.values

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
    X=df.values

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


