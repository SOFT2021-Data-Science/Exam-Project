<template>
  <div class="about">
    <h1>About</h1>
    <p>
      This site is made with the intent to use data science algorithms to gain a better understanding of trends within suicide rates throughout the years and in various regions and between the genders.<br>
      To achieve this purpose, two datasets have been chosen: The first being Kaggle  and the second being from WHO . The dataset from kaggle covers countries in the world, whereas the sdg dataset from who covers all continents.<br>
      Those dataset can be selected as parameters, for three different data science algorithms: Linear regression, polynomial regression and K-Means.<br>
      Linear regression has the disadvantage that it doesn't work well with some datasets if the data is irregular and nonlinear, therefor we also implemented Polynomial Regression to cover this issue.<br>
      With the Polynomial regression model we attempt to predict future suicide trends on both datasets, however the predictions accuracy depends on the r2 score that is generated with each run. The closer the r2 score is to 1, the higher the chance is that our prediction valid (at least in theory).<br>
      K-Means purpose on the site, is to find different groupings of suicide rates throughout the years.<br>
      We’ve chosen to write about this subject, so people can gain insight into suicidal trends in different countries and genders.    </p>
    <h2>Description of datasets</h2>
    <h3>SDG</h3>
    <p>
      Is a dataset of the suicides rates for the different regions around the
      world from 2000-2019, The dataset is fielded in a way that you can choose.
    </p>
    <ul>
      <li>
        <b>Region</b>: Is used to filter the dataset by region: fx. Africa or
        Europe.
      </li>
      <li>
        <b>Gender</b>: This field specifies if you want data from male, female
        or both.
      </li>
      <li><b>Preview</b>: Here you can choose between preview and template.</li>
      <li>
        <b>Preview</b>: If you choose this it will give you a static graph made
        from the chosen values.
      </li>
      <li>
        <b
          >Template: If you choose this it will give you an interactable graph
          made from the chosen values, where you can zoom in and out on the
          graph.</b
        >
      </li>
    </ul>
    <h3>KAGGLE</h3>
    <p>
      Is a dataset of the suicides rates for the different countries around the
      world from 1985-2016, The dataset is fielded in a way that you can choose.
    </p>
    <ul>
      <li>
        <b>Region</b>: Is used to filter the dataset by country: fx. Denmark or
        Finland.
      </li>
      <li>
        <b>Gender</b>: This field specifies if you want data from male or
        female.
      </li>
      <li><b>Preview</b>: Here you can choose between preview and template.</li>
      <li>
        <b>Preview</b>: If you choose this it will give you a static graph made
        from the chosen values.
      </li>
      <li>
        <b>Template:</b> If you choose this it will give you an interactable
        graph made from the chosen values, where you can zoom in and out on the
        graph.
      </li>
    </ul>
    <h2>Diagram Descriptions</h2>
    <ul>
      <li>Linear Regression</li>
      <li>Polynomial regression</li>
      <li>Kaggle/Clustering</li>
      <li>Kaggle/Elbow</li>
      <li>Compare Countries/Regions Comparison</li>
      <li>Compare Country/Region Comparison genders</li>
    </ul>
    <ul>
      <li>
        <p>
          We use R² to measurer validity of our Diagram
          R² is a metric of correlation. Correlation is measured by “r” and it
          tells us how strongly two variables can be related. A correlation
          closer to +1 means a strong relationship in the positive direction,
          while -1 means a stronger relationship in the opposite direction. A
          value closer to 0 means that there is not much of a relationship
          between the variables. R-squared is closely related to correlation.
          source:
          https://towardsdatascience.com/data-science-explaining-r%C2%B2-in-statistics-6f34e7f0a9bb
        </p>
        <p>
          <b>Linear regression</b>
          “A linear regression line has an equation of the form Y = a + bX, where X is the explanatory variable and Y is the dependent variable. The slope of the line is b, and a is the intercept (the value of y when x = 0). “
          
          
          http://www.stat.yale.edu/Courses/1997-98/101/linreg.htm 
        </p>
        <p>
          <b>Polynomial regression</b>
          “Polynomial regression is a regression algorithm which models the relationship between dependent and the independent variable is modeled such that the dependent variable Y is an nth degree function of the independent variable Y.”

          “The formula of Polynomial Regression is, in this case, is modeled as:”<br />
          <img src="@/assets/p1.png" alt=""><br />

          “Where y is the dependent variable and the betas are the coefficient for different nth powers of the independent variable x starting from 0 to n. The calculation is often done in a matrix form as shown below:”<br />
          <img src="@/assets/p2.png" alt=""><br />

          
          https://mindmajix.com/polynomial-regression
        </p>
        <p>
          <b>K-Means clustering</b>
          “K-Means clustering intends to partition n objects into k clusters in which each object belongs to the cluster with the nearest mean. This method produces exactly k different clusters of greatest possible distinction. The best number of clusters k leading to the greatest separation (distance) is not known as a priori and must be computed from the data. The objective of K-Means clustering is to minimize total intra-cluster variance, or, the squared error function:”<br />
          
          <img src="@/assets/k1.png" alt=""><br /> 
          <br />
          
         
          <br /> 
          “The Elbow Method is one of the most popular methods to determine this optimal value of k.”<br />
          <br /> 
          
           https://www.saedsayad.com/clustering_kmeans.htm<br />
          https://www.geeksforgeeks.org/elbow-method-for-optimal-value-of-k-in-kmeans/ 
        </p>

        <p>
          <b>Compare Countries/Regions Comparison</b>
          This diagram compares two Countries/Regions suicide rate for females or males. Pr 100K
        </p>
        <p>
          <b>Compare Country/Region Comparison genders</b>
          This diagram compares Country/Region suicide rate between the genders. Pr 100K
        </p>
        
      </li>
    </ul>
  </div>
</template>

