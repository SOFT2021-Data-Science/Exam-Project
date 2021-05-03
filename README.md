# Exam-Project

Server: mutezone.site





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



Stage 1: Business Case Foundation
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

Stage 2.

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
   <li>e. Create a prototype of data story</li>
</ul>

1. Export your solution in a file and upload it to your git repository.
<p>Done. In this repository</p>
