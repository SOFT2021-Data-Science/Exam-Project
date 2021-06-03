<template>
  <div class="about">
    <h1>About</h1>
    <p>
      <br>This site is made with the intent to use data science algoriments to gain a better understanding of trends within suicide rateds throughout the years and in various regions and between the sexes.
      <br>To achieve this purpose, this site uses two main dataset, Two datasets have been chosen. One from Kaggle and one from WHO. Kaggle covers all countries in the world, while the sdg dataset(WHO) covers all continents. 
      <br>Those dataset can be selected as parameters, for two different data science algoriments Linear regression, polynomial regression and K-Means. 
      <br>K-Means purpose on the site, is to find different groupings of suicide rates throughout the years. 
      <br>On this site we use both Linear regression and Polynomial regression. Linear regression has the disadvantage that it doesn't work with some datasets if the dataset is too curved og bending, this is where Polynomial regression would be better. 
      <br>Linear regression and Polynomial regression is used to give future prediction of the different trends, within the suicide rates acording to the different dataset. This makes for great information, because it can predict the logical next step of the different suicide rates. Which can be compared with the real future suicide rates, 
      <br>to see if there is a unatural rise of fall in suicides. Which inturn can lead catching faster bad trends in rising suicide rates.
    </p>
    <h2>Description of datasets</h2>
    <h3>SDG</h3>
    <p>Is a dataset of the suicides rates for the different regions around the world from 2000-2019, The dataset is fielded in a way that you can choose.</p>
    <ul>
      <li><b>Region</b>: Is used to filter the dataset by region: fx. Africa or Europe.</li>
      <li><b>Gender</b>: This field specifies if you want data from male, female or both.</li>
      <li><b>Preview</b>: Here you can choose between preview and template.</li>
      <li><b>Preview</b>: If you choose this it will give you a static graph made from the chosen values.</li>
      <li><b>Template: If you choose this it will give you an interactable graph made from the chosen values, where you can zoom in and out on the graph.</b></li>
    </ul>
    <h3>KAGGLE</h3>
    <p>Is a dataset of the suicides rates for the different countries around the world from 1985-2016, The dataset is fielded in a way that you can choose.</p>
    <ul>
      <li><b>Region</b>: Is used to filter the dataset by country: fx. Denmark or Finland.</li>
      <li><b>Gender</b>: This field specifies if you want data from male or female.</li>
      <li><b>Preview</b>: Here you can choose between preview and template.</li>
      <li><b>Preview</b>: If you choose this it will give you a static graph made from the chosen values.</li>
      <li><b>Template:</b> If you choose this it will give you an interactable graph made from the chosen values, where you can zoom in and out on the graph.</li>
    </ul>
    <h2>Diagram Descriptions</h2>
    <ul>
      <li>LinearRegression</li>
      <li>Kaggle/Clustering</li>
      <li>Kaggle/Elbow</li>
    </ul>

    <ul>
      <li>
        <p>
        R² R-squared is a metric of correlation. Correlation is measured by “r” and it tells us how strongly two variables can be related. A correlation closer to +1 means a strong relationship in the positive direction, 
        while -1 means a stronger relationship in the opposite direction. A value closer to 0 means that there is not much of a relationship between the variables. R-squared is closely related to correlation.
        source: https://towardsdatascience.com/data-science-explaining-r%C2%B2-in-statistics-6f34e7f0a9bb
        </p>
      </li>
    </ul>
  </div>
</template>

