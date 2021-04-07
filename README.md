# zillow-clustering-project

Clustering Project: Drivers of Error in Zillow Zestimates

Data Science Team Members: Gabby Broussard and Barbara Marques

#### Project Summary:

Our team has been asked to analyze Zillow data on single unit/single family properties with transaction dates in 2017 to discover the drivers of errors in Zillow's Zestimates. 

Data Source: Zillow database on Codeup's data server.

#### Project Goals: 
- Deliver a notebook presentation of models used to isolate drivers of error in Zillow Zestimates.
- Use clustering methodologies to engineer new features and visualize factors that contribute to log errors in Zillow Zestimates.

All files referenced in this presentation are available in the github repository for this project: https://github.com/B-G-Clustering/zillow-clustering-project

#### Hypotheses:

- H$_{0}$: There is no significant difference in logerror for properties in LA County vs Orange County vs Ventura County.  --> REJECT
  H$_{a}$: Log error is significantly different among the counties of LA County, Orange County and Ventura County.
  alpha(𝛼): 1 - confidence level (95% confidence level -> 𝛼=.05 )
    - Anova
    - We reject the null hypothesis that there is no significant difference in logerror for properties in LA County vs Orange County vs Ventura County
    
- H$_{0}$: There is no difference in log error based on a property's square footage. --> REJECT
  H$_{a}$: Properties with square footage less than 2800 square footage have a lower log error than larger properties.
  alpha(𝛼): 1 - confidence level (95% confidence level -> 𝛼=.05 )
    - Pearson R Correlation
    - We reject the null hypothesis that there is no difference in log error based on a properties square footage.
    
    
- H$_{0}$:
  H$_{a}$:
  
  alpha(𝛼): 1 - confidence level (95% confidence level -> 𝛼=.05 )



#### Recommendation & Takeaways:

- Overall, predicting log error is difficult to perform due to none of the features having a strong relationship with log error.<br>

- This could be caused by over cleaning data, not having enough outside features collected, or changing social trends in property buying. <br>

- Out of the available data and clusters, cluster_location_1 was built from latitude, longitude, cola, fips. This was chosen used as the best feature for modeling.<br>

#### Given more Time and Resources, I would:


- Due to time constraints, we were unable to model Test on lassoLars. Under previous iterations, the best performing model was the quadratic model just slightly outperforming baseline. With this iteration, none of the models outperformed baseline.<br>

- Given more time and resources, model on cluster_location_2 to see if that cluster predicts logerror better than cluster_location_1. We would also identify the characteristics of the clusters. 





#### Progression through the Data Science Pipeline: 
``` PLAN -> ACQUIRE -> PREPARE -> EXPLORE -> MODEL -> DELIVER ```

Each step in our process is recorded and staged on a Trello board at: https://trello.com/b/N9q5dtX3/zillow-clustering-project

```Plan:```
- Create GitHub organization and set up GitHub repo, to include readme.md and .gitignore.
- Use Sequel to investigate the database and compose an appropriate query
- Brainstorm a list of questions and form hypotheses about how variables might impact one another. 

```Acquire:```
- Read data from Zillow’s database located on Codeup’s SQL Server into a Pandas dataframe to be analyzed using Python.
- Created a function, ```acquire(df)```, as a reproducible component for acquiring necessary data.
- Created a .csv file of acquired data.

```Prepare:```
- Carefully reviewed data, identifying any missing, erroneous, or invalid values. 
- Explored value counts of the dataframe and visualized distribution of univariate data 
- Created and called a function, ```wrangle_zillow```, as a reproducible component that cleans/prepares data for analysis by: renames columns, handling missing values, adjusts data types, handles any data integrity
- Split the data into train, validate and test sets.


```Explore:```
- Visualized all combination of variables to explore relationships.
- Tested for independent variables that correlate with correlate with log error.
- Developed hypotheses and ran statistical tests to accept or reject null hypotheses.
- Summarized takeaways and conclusions.
- Scaled data using MinMax scaler.
- Used clustering methodologies to create new features to model on.
- Ran additional statistical tests on clustered data.

```Model:``` 
- Developed a baseline model.
- Modeled train and validate data on OLS, Lasso Lars, and Polynomial Regression. 
- Modeled test on Polynomial Regression.


```Deliver:```
- Clearly document all code in a reproducible Jupyter notebook called Zillow_Clustering_Project.


#### Instructions for Reproducing Our Findings:

1.  Start by cloning the github repository on your From your terminal command line, type git@github.com:B-G-Clustering/zillow-clustering-project.git

2.  Download the following files from https://github.com/B-G-Clustering/zillow-clustering-project to your working directory:  
 - Zillow_Clustering_Project.ipynb
 - wrangle.py
 - explore.py
  
3.  You will also need you a copy of your personal env file in your working directory:
 - This should contain your access information (host, user, password) to access Codeup's database in MySQL

4. Run the Jupyter notebook, Zillow_Regression_Project, cell by cell, to reproduce my analysis.


#### ```Data Dictionary of Variables Used in Analysis```

| Attribute | Definition | Data Type |
| ----- | ----- | ----- |
|acres|Square footage of lot converted to acres (43560 sq ft = 1 acre)|float64|
|age|Number of years from original construction until the home sold in 2017.| float64 |
|bathrooms| Number of bathrooms in home, including fractional bathrooms | float64 |
|bedrooms|Number of bedrooms in home| float64 |
|cola|Designates whether properties are located within the City of Los Angeles|int64|
|fips|Federal Information Processing Standard Code. This code identifies the county in which the home is located. 6037: Los Angeles County, 6059: Orange County, 6111: Ventura County|int64 |
|land_dollar_per_sqft|land tax value divided by lot size|float64|
|land_tax_value| The 2017 total tax assessed value of the land|float64|
|latitude| Latitude of the middle of the parcel multiplied by 10e6|float64 |
|log_error| The log(Zestimate) - log(SalePrice)  |  float64  |
|longitude| Longitude of the middle of the parcle multiplied by 10e6|float64|
|lot_size|Area of the lot in square feet| int64 |
|parcel_id| Unique identifier for parcels (lots) | object |
|structure_dollar_per_sqft|structure tax value divided by square feet|float64|
|structure_tax_value| The 2017 total tax assessed value of the structure|float64|
|square_feet|Calculated total finished living area of the home| float64|
|tax_amount|The calculated amount of tax due in 2017|float64|
|taxrate| Calculated based on taxed amount and assessed value of home |float64|
|tax_value| The 2017 total tax assessed value of the parcel | float64 |
|taxes|The total property tax assessed for the assessment year|float64|
|zip_code| Zip code in which the home is located| int64 |

 



