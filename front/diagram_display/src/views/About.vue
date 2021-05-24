<template>
  <div class="about">
    <h1>About</h1>
    <p>
      This site is made with the intent to use data science algoriments to gain a better understanding of trends within suicide rateds throughout the years and in various regions and between the sexes.<br>
      To achieve this purpose, this site uses two main dataset, United States(Kaggle) fukuset dataset and a world wide (stg) dataset. Those dataset can be selected as parameters, for two different data science algoriments Linear regression, polynomial regression and K-Means. <br>
      K-Means purpose on the site, is to find different groupings of suicide rateds throughout the years. Which can be useful insight, because of the way it may show patterns that can lead to finding a common denominator for the group, which can be useful information in future studies. <br>
      On this site we use both Linear regression and Polynomial regression. Linear regression has the disadvantage that it doesn't work with some datasets if the dataset is too curved og bending, this is where Polynomial regression would be better. <br>
      Linear regression and Polynomial regression is used to give future prediction of the different trends, within the suicide rates acourding to the diffent dataset. This makes for great information, because it can predict the logical next step of the different suicide rates. Which can be compared with the real future suicide rates, to see if there is a unatuel rise of fall in suicides. Which inturn can lead catching faster bad trends in rising suicide rates.<br>
    </p>
    <h2>Description of datasets</h2>
    <h3>SDG</h3>
    <p>Is a dataset of the suicides rates for the different regions around the world from 2000-2019, The dataset is fielded in a way that you can choose.</p>
    <ul>
      <li><b>Region</b>: Is used to filter the dataset by region: fx. Africa or Europe.</li>
      <li><b>Gender</b>: This field specifies if you want data from male, female or both.</li>
      <li><b>Preview</b>: Here you can choose between preview and template.</li>
      <li><b>Preview</b>: If you choose this it will give you a static graph made from the chosen values.</li>
      <li><b>Tempalte: If you choose this it will give you an interactable graph made from the chosen values, where you can zoom in and out on the graph.</b></li>
    </ul>

    <h3>KAGGLE</h3>
    <p>Is a dataset of the suicides rates for the different countries around the world from 1985-2016, The dataset is fielded in a way that you can choose.</p>
    <ul>
      <li><b>Region</b>: Is used to filter the dataset by country: fx. Denmark or Finland.</li>
      <li><b>Gender</b>: This field specifies if you want data from male or female.</li>
      <li><b>Preview</b>: Here you can choose between preview and template.</li>
      <li><b>Preview</b>: If you choose this it will give you a static graph made from the chosen values.</li>
      <li><b>Tempalte: If you choose this it will give you an interactable graph made from the chosen values, where you can zoom in and out on the graph.</b></li>
    </ul>
  </div>
</template>

