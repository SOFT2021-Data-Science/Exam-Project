# Exam-Project

## Deployed at: [mutezone.site](http://mutezone.site)





Focus:

Suicide rates. Male / Females. Rural / urban / metropolitan. Population density?


What is the focus?
We're interested in the suicide rates of different groups, such as gender, area, race, time, etc. 
Our primary scope will be focused on USA, since USA has the richest amount of data available.

Why is it interesting?
Suicide is supposedly the 10th leading cause of death in 2017. There are large differences between the categories defined above.
Informing suicide prevention organisations and other interested parts about these trends, 
should be able to generate some clarity about the importance of the matter, and what we can do to prevent in the future.

What outcome do you expect from your research
The suicide rate among isolated individuals will be higher. Cases of prolonged mass isolation are limited. We can't use Covid-19 data because of lack of data. 
Gathering information about other cases might provide insight, about how the possible trends in suicide rates in America fluxes with isolation. 

Who may be the user of the results?
The results are primarily targeted towards interested organisations, herein suicide prevention organisations.
The statistics will be publically available.

## Stage 1: Business Case Foundation
1. Collect ideas and define a business or social domain, where data science can bring a value.

Suicide rates. Male / Female. Rural

2. Search Internet and get inspired by sources of information, related to your ideas.
3. Formulate context, purpose, questions, and hypotheses for a data science experiment.
4. Technology
a. Select and install software tools and development environments.
b. Create a Github repository, which will host all project components during all stages of the
development and implementation process.
c. Create and upload a .md file as an initial release of the project, which contains brief
annotation of your ideas, in minimum four sentences, telling:
• what is in the focus of your interest?
• why is it interesting?
• which outcome do you expect from your research?
• who may be a user of the results?

## Stage 2.

1. csv files found, saved and sources documented in "./resources/datasets". Further exploration of population density and urbanization required. Consider the necessary for prototyping and proof of concepts.

2. Shared repository on github. Data stored on server in cloud. Data is shared between docker containers through volumes. The paths to these volumes change from development to production versions. The correct path is assigned through environment variables. The project uses an ELT approach, due to the multiple ways the data can be interpreted.

3.
<ul>
   <li>a. Decide on data processing parameters and methods</li>
   <p>
    Machine learning model predictions allows us to make highly accurate guesses as to the likely outcomes of a question based on historical data, therefore we plan on implementing both the Forecast Model and the Clustering Model. K-means.
    Basic visual representation.
   </p>
    <p>
    Available parameters include "age", "gender", "location/urbanization", "population density", "race", "geolocation"</p>
   <li>b. Choose data visualization techniques</li>
   <p>Matplotlib will generate the images. Images will be saved ./resources/out. Vue will show the image on the home page.</p>
   <li>c. Create visual representations</li>
   <p>Visual representations can be found as .png files in ./resources/out</p>
   <li>d. Create dashboards </li>
   <p>Dashboards can be run in the frontend with npm run serve</p>
   <p>More variations will be added over time as we implement more functionalities</p>
   <li>e. Create a prototype of data story</li>
   <p>Dashboard fetches information from the backend, which is the full setup for the data story. Again, the dashboard will be populated with options as the project progresses.</p>
</ul>

Machine Learning Algorithms:
Linear Regression & Clustering : [Kaggle](back/diagram_webservice/src/logic/kaggle.py) & [sdg](back/diagram_webservice/src/logic/sdg.py)


##  Stage 4: Immersive Analytics and Visualisation

### Elaborate on the benefits of applying better visualisation techniques for data analytics.
Better data visualisation allows for greater and faster understanding for big and complex datasets. This is because we as humans are better at spotting patterns when data is presented in easy to graph visuals, such as diagrams. Another method that makes the dataset easier to comprehend, is using the visuals to tell a story that the viewers can follow.  

This is why when you have to represent specific concepts and new ideas it’s ideal to use better visualisation techniques that can create a narrative for the viewers to follow. This can better be achieved with 3D or VR/AR/MR visualisation. These tools can make it easier for the viewers to see new insights in the data that they otherwise would have missed if not for the new layer of visualisation.  

A VR visualisation that we could apply to our project could be that we made a world map where you could click on the different regions on the map to get a 3D graph of the suicide rates in that specific region.  

This would help the viewer to get a better scope of the dataset because of the intractability, while also giver the opportunity to better compare the the different regions suicide rates to notice different trendes in amound the data.  

Example:
![img](/resources/visualisation.png)

## notes
./resources/out is generated the first time [aliases.py](back/diagram_webservice/src/utils/aliases.py) is imported.


This directory gets populated with functions from [Kaggle](back/diagram_webservice/src/logic/kaggle.py) & [sdg](back/diagram_webservice/src/logic/sdg.py)
Example: kaggle_linear_regression with "savefig"

## Stage 5

### Problem objectives
Make the differences in suicide among different sets of people known
 
### Motivation
Suicide rates are hints of the psychological welfare of civilizations. There are some clear differences when it comes to location/gender/race. Furthermore, isolation has an impact on suicidal tendencies, which can be seen depending on urbanization. The initial hypothesis was, that suicide rates would increase during Corona.

### Theoretical Foundation
“The goal of a theoretical framework is to present and explain the theories and models that other researchers have already developed.” - *[[source]](https://www.youtube.com/watch?v=4y1BAqOnhMM)*

Our project is not developed from any prior theories or models. Bringing new theoretical research was never intended to be part of the process of the development of our project. The goal of this project was to take datasets of suicide rates from around the world, and transform it in a way which would provide a clearer overview of the current situation, as well as attempt to predict how the situation would change in the future. This includes making simple comparisons, and making future prediction, to give insight of suicide trends.

### Argumentation of Choices
We have chosen K-Means to find different groupings of suicide rates throughout the years, which can help in identifying trends in suicide rates. We also use both Linear regression and Polynomial regression.
Linear regression and Polynomial regression is used to give future prediction of the different trends, within the suicide rates according to the different dataset. This makes for great information, because it can predict the logical next step of the different suicide rates. Which can be compared with the real future suicide rates,
to see if there is an unnatural rise of fall in suicides. Which inturn can lead catching faster bad trends in rising suicide rates.
We have chosen to focus on Polynomial regression because Linear regression has the disadvantage that it doesn't work with some datasets if the dataset is too curved og bending, this is where Polynomial regression would be better.

### Code
The code can be found in this repository.
Specifically, the machine learning algorithms that we have made can be found in these files: [Kaggle](back/diagram_webservice/src/logic/kaggle.py) & [sdg](back/diagram_webservice/src/logic/sdg.py).

### Artifacts
Linear regression   
polynomial regression with future prediction  
k-means clustering  
K-means with elbow  
*All of our machine learning algorithms outputs data to a pot.*  

### Outcomes:
- A REST api with functionalities which allows the user to generate multiple images depending on various parameters.
- There’s a small framework-like setup, which allows for easy addition of new models and datasets depending on what is required. 
- Continuous deployment has been integrated in the solution. Secrets are stored in github actions. Frontend is deployed at http://mutezone.site. 
- Backend is deployed at http://mutezone.site:8000/ 
- Various machine learning models:
   - Linear regression
   - Polynomial regression
   - k-means clustering
   - k-means elbow
- Two basic models for comparison:
   - Country/region vs country/region differences
   - Gender differences
- The models are implemented for both the SDG and Kaggle datasets.

## Implementation Instructions
1. Clone the project.
2. Open the cloned directory in a terminal.
3. Have docker installed.
4. Type command: ***```docker-compose up```***