# zillow-clustering-project
Clustering Project: Drivers of Error in Zillow Zestimates

#### Project Summary:

Our team has been asked to analyze Zillow data on single unit/single family properties with transaction dates in 2017 to discover the drivers of errors in Zillow's zestimates. 

Data Source: Zillow database on Codeup's data server.

Data Science Team Members: Gabby Broussard and Barbara Marques

All files referenced in this presentation are available in the github repository for this project: https://github.com/B-G-Clustering/zillow-clustering-project

#### Hypotheses:

- H$_{0}$: There is no difference in log error based on a properties square footage.
  H$_{a}$:  Properties with a square footage less than 2800 square footage have a lower log error than larger properties.
  alpha ( 𝛼 ): 1 - confidence level (95% confidence level -> 𝛼=.05 )

- H$_{0}$: There is no difference in median log error in properties built in different years. 
  H$_{a}$: Properties that were built after 1975 have a higher median log error than properties built before 1975.
  alpha ( 𝛼 ): 1 - confidence level (95% confidence level -> 𝛼=.05 )

- H$_{0}$: There is no correlation between latitude and log error.
  H$_{a}$: Properties that are more southern have a higher log error.
  alpha ( 𝛼 ): 1 - confidence level (95% confidence level -> 𝛼=.05 )



#### Recommendation & Takeaways:

- .

#### Given more Time and Resources, I would:

- 





#### Progression through the Data Science Pipeline: 
``` PLAN -> ACQUIRE -> PREPARE -> EXPLORE -> MODEL -> DELIVER ```

Each step in the process is recorded and staged on a Trello board at: https://trello.com/b/N9q5dtX3/zillow-clustering-project


```Plan:```
- Create GitHub organization and set up GitHub repo, to include readme.md and .gitignore.
- Use Sequel to investigate the database and compose an appropriate query
- Brainstorm a list of questions and form hypotheses about how variables might impact one another. 

```Acquire:```
- Read data from Zillow’s own database located on Codeup’s SQL Server into a Pandas dataframe to be analyzed using Python.
- Created a function, ```acquire(df)```, as a reproducible component for acquiring necessary data.

```Prepare:```
- Carefully reviewed data, identifying any missing, erroneous, or invalid values. 
- Explored value counts of the dataframe and visualized distribution of univariate data 
- Created and called a function, ```prep_zillow```, as a reproducible component that cleans/prepares data for analysis by: renames columns, handling missing values, adjusts data types, handles any data integrity
- Created and called a function, ```train_validate_test_split```, that splits the data into train, validate and test sets.
- Numeric data was scaled using MinMax scaler.
- Created a module ```wrangle_zillow.py``` which stores code for functions that acquire and prepare data.

```Explore:```
- Visualize all combination of variables to explore relationships.
- Tested for independent variables that correlate with tax value.
- Created a module, ```explore.py```, which stores code for functions to explore data.
- Developed hypotheses and ran statistical tests: t-test and correlation, to accept or reject null hypotheses.
- Summarized takeaways and conclusions.

```Model:``` 
- Developed a baseline model.
- Developed a regression model that performs better than the baseline
- Documented algorithms and hyperparameters used.
- Plotted the residuals and documented evaluation metrics (SSE, RMSE, or MSE).

```Deliver:```
- Clearly documented all code in a reproducible Jupyter notebook called Zillow_Clustering_Project.


#### Instructions for Reproducing My Findings:

1.  Start by cloning the github repository on your From your terminal command line, type git@github.com:B-G-Clustering/zillow-clustering-project.git

2.  Download the following files from https://github.com/B-G-Clustering/zillow-clustering-project to your working directory:  
 - Zillow_Clustering_Project.ipynb
 - wrangle.py
 - explore.py
  
3.  You will also need you a copy of your personal env file in your working directory:
 - This should contain your access information (host, user, password) to access Codeup's database in MySQL

4. Run the Jupyter notebook, Zillow_Regression_Project, cell by cell, to reproduce my analysis.


#### Data Dictionary of Variables Used in Analysis

| Attribute | Definition | Data Type |
| ----- | ----- | ----- |
|longitude| Longitude of the middle of the parcle multiplied by 10e6|int64|
|latitude| Latitude of the middle of the parcel multiplied by 10e6|int64 |
|log_error| The log(Zestimate) - log(SalePrice)  |  int64  |
|tax_value| The 2017 total tax assessed value of the parcel | int64 |
|parcel_id| Unique identifier for parcels (lots) | object |
|bathrooms| Number of bathrooms in home, including fractional bathrooms | int64 |
|square_feet|Calculated total finished living area of the home| int64|
|bedrooms|Number of bedrooms in home| int64 |
|lot_size|Area of the lot in square feet| int64 |
|zip_code| Zip code in which the home is located| int64 |
|fips|Federal Information Processing Standard Code. This code identifies the county in which the home is located. 6037: Los Angeles County, 6059: Orange County, 6111: Ventura County|int64 |
|age|Number of years from original construction until the home sold in 2017.| int64 | 
|taxes|The total property tax assessed for the assessment year|float64|
|tax rate| Calculated based on taxed amount and assessed value of home |float64|

