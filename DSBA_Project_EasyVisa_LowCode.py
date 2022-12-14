#!/usr/bin/env python
# coding: utf-8

# ## EasyVisa Project
# ***Marks: 60***

# ## Problem Statement

# ### Context:
# 
# Business communities in the United States are facing high demand for human resources, but one of the constant challenges is identifying and attracting the right talent, which is perhaps the most important element in remaining competitive. Companies in the United States look for hard-working, talented, and qualified individuals both locally as well as abroad.
# 
# The Immigration and Nationality Act (INA) of the US permits foreign workers to come to the United States to work on either a temporary or permanent basis. The act also protects US workers against adverse impacts on their wages or working conditions by ensuring US employers' compliance with statutory requirements when they hire foreign workers to fill workforce shortages. The immigration programs are administered by the Office of Foreign Labor Certification (OFLC).
# 
# OFLC processes job certification applications for employers seeking to bring foreign workers into the United States and grants certifications in those cases where employers can demonstrate that there are not sufficient US workers available to perform the work at wages that meet or exceed the wage paid for the occupation in the area of intended employment.
# 
# ### Objective:
# 
# In FY 2016, the OFLC processed 775,979 employer applications for 1,699,957 positions for temporary and permanent labor certifications. This was a nine percent increase in the overall number of processed applications from the previous year. The process of reviewing every case is becoming a tedious task as the number of applicants is increasing every year.
# 
# The increasing number of applicants every year calls for a Machine Learning based solution that can help in shortlisting the candidates having higher chances of VISA approval. OFLC has hired the firm EasyVisa for data-driven solutions. You as a data  scientist at EasyVisa have to analyze the data provided and, with the help of a classification model:
# 
# * Facilitate the process of visa approvals.
# * Recommend a suitable profile for the applicants for whom the visa should be certified or denied based on the drivers that significantly influence the case status. 
# 
# ### Data Description
# 
# The data contains the different attributes of employee and the employer. The detailed data dictionary is given below.
# 
# * case_id: ID of each visa application
# * continent: Information of continent the employee
# * education_of_employee: Information of education of the employee
# * has_job_experience: Does the employee has any job experience? Y= Yes; N = No
# * requires_job_training: Does the employee require any job training? Y = Yes; N = No 
# * no_of_employees: Number of employees in the employer's company
# * yr_of_estab: Year in which the employer's company was established
# * region_of_employment: Information of foreign worker's intended region of employment in the US.
# * prevailing_wage:  Average wage paid to similarly employed workers in a specific occupation in the area of intended employment. The purpose of the prevailing wage is to ensure that the foreign worker is not underpaid compared to other workers offering the same or similar service in the same area of employment. 
# * unit_of_wage: Unit of prevailing wage. Values include Hourly, Weekly, Monthly, and Yearly.
# * full_time_position: Is the position of work full-time? Y = Full Time Position; N = Part Time Position
# * case_status:  Flag indicating if the Visa was certified or denied

# ### **Please read the instructions carefully before starting the project.** 
# This is a commented Jupyter IPython Notebook file in which all the instructions and tasks to be performed are mentioned. 
# * Blanks '_______' are provided in the notebook that 
# needs to be filled with an appropriate code to get the correct result. With every '_______' blank, there is a comment that briefly describes what needs to be filled in the blank space. 
# * Identify the task to be performed correctly, and only then proceed to write the required code.
# * Fill the code wherever asked by the commented lines like "# write your code here". Running incomplete code may throw error.
# * Please run the codes in a sequential manner from the beginning to avoid any unnecessary errors.
# * Add the results/observations (wherever mentioned) derived from the analysis in the presentation and submit the same.

# ## Importing necessary libraries

# In[2]:


# this will help in making the Python code more structured automatically (good coding practice)


import warnings

warnings.filterwarnings("ignore")

# Libraries to help with reading and manipulating data
import numpy as np
import pandas as pd

# Library to split data
from sklearn.model_selection import train_test_split

# libaries to help with data visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Removes the limit for the number of displayed columns
pd.set_option("display.max_columns", None)
# Sets the limit for the number of displayed rows
pd.set_option("display.max_rows", 100)


# Libraries different ensemble classifiers
from sklearn.ensemble import (
    BaggingClassifier,
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
    StackingClassifier,
)

get_ipython().system('pip install xgboost')
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier

# Libraries to get different metric scores
from sklearn import metrics
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

# To tune different models
from sklearn.model_selection import GridSearchCV


# ## Importing Dataset

# In[3]:


visa = pd.read_csv(r"C:\Users\harri\OneDrive\Documents\Great Learning Projects\Project 5\EasyVisa.csv") ##  Fill the blank to read the data


# In[3]:


# copying data to another variable to avoid any changes to original data
data = visa.copy()


# ## Overview of the Dataset

# ### View the first and last 5 rows of the dataset

# In[4]:


data.head() ##  view top 5 rows of the data


# In[5]:


data.tail() ##  view last 5 rows of the data  


# ### Understand the shape of the dataset

# In[6]:


data.shape ##  to view dimensions of the data


# ### Check the data types of the columns for the dataset

# In[ ]:


data.info()


# In[8]:


# checking for duplicate values
data.duplicated().sum() ##  to check duplicate entries in the data


# ## Exploratory Data Analysis

# #### Let's check the statistical summary of the data

# In[9]:


data.describe().T ##  to print the statistical summary of the data


# #### Fixing the negative values in number of employees columns

# In[10]:


data.loc[data['no_of_employees']<0] ## check negative values in the employee column


# In[11]:


# taking the absolute values for number of employees
data["no_of_employees"] = np.abs(data["no_of_employees"]) ## Write the function to convert the values to a positive number


# #### Let's check the count of each unique category in each of the categorical variables

# In[12]:


# Making a list of all catrgorical variables
cat_col = list(data.select_dtypes("object").columns)

# Printing number of count of each unique value in each column
for column in cat_col:
    print(data[column].value_counts())
    print("-" * 50)


# In[14]:


# checking the number of unique values
data["case_id"].unique ## check unique values in the mentioned column


# In[15]:


data.drop(["case_id"], axis=1, inplace=True) ## drop 'case_id' column from the data


# ### Univariate Analysis

# In[16]:


def histogram_boxplot(data, feature, figsize=(15, 10), kde=False, bins=None):
    """
    Boxplot and histogram combined

    data: dataframe
    feature: dataframe column
    figsize: size of figure (default (15,10))
    kde: whether to show the density curve (default False)
    bins: number of bins for histogram (default None)
    """
    f2, (ax_box2, ax_hist2) = plt.subplots(
        nrows=2,  # Number of rows of the subplot grid= 2
        sharex=True,  # x-axis will be shared among all subplots
        gridspec_kw={"height_ratios": (0.25, 0.75)},
        figsize=figsize,
    )  # creating the 2 subplots
    sns.boxplot(
        data=data, x=feature, ax=ax_box2, showmeans=True, color="violet"
    )  # boxplot will be created and a triangle will indicate the mean value of the column
    sns.histplot(
        data=data, x=feature, kde=kde, ax=ax_hist2, bins=bins
    ) if bins else sns.histplot(
        data=data, x=feature, kde=kde, ax=ax_hist2
    )  # For histogram
    ax_hist2.axvline(
        data[feature].mean(), color="green", linestyle="--"
    )  # Add mean to the histogram
    ax_hist2.axvline(
        data[feature].median(), color="black", linestyle="-"
    )  # Add median to the histogram


# #### Observations on number of employees

# In[17]:


histogram_boxplot(data, "no_of_employees")


# #### Observations on prevailing wage

# In[18]:


histogram_boxplot(data, 'prevailing_wage') ## create histogram_boxplot for prevailing wage


# In[19]:


# checking the observations which have less than 100 prevailing wage
data.loc[data['prevailing_wage']<100] ## find the rows with less than 100 prevailing wage


# In[20]:


data.loc[data["prevailing_wage"] < 100, "unit_of_wage"].count() ## get the count of the values in the mentioned column


# In[21]:


# function to create labeled barplots


def labeled_barplot(data, feature, perc=False, n=None):
    """
    Barplot with percentage at the top

    data: dataframe
    feature: dataframe column
    perc: whether to display percentages instead of count (default is False)
    n: displays the top n category levels (default is None, i.e., display all levels)
    """

    total = len(data[feature])  # length of the column
    count = data[feature].nunique()
    if n is None:
        plt.figure(figsize=(count + 2, 6))
    else:
        plt.figure(figsize=(n + 2, 6))

    plt.xticks(rotation=90, fontsize=15)
    ax = sns.countplot(
        data=data,
        x=feature,
        palette="Paired",
        order=data[feature].value_counts().index[:n],
    )

    for p in ax.patches:
        if perc == True:
            label = "{:.1f}%".format(
                100 * p.get_height() / total
            )  # percentage of each class of the category
        else:
            label = p.get_height()  # count of each level of the category

        x = p.get_x() + p.get_width() / 2  # width of the plot
        y = p.get_height()  # height of the plot

        ax.annotate(
            label,
            (x, y),
            ha="center",
            va="center",
            size=12,
            xytext=(0, 5),
            textcoords="offset points",
        )  # annotate the percentage

    plt.show()  # show the plot


# #### Observations on continent

# In[22]:


labeled_barplot(data, "continent", perc=True) 


# #### Observations on education of employee

# In[23]:


labeled_barplot(data, 'education_of_employee')  ## create labeled_barplot for education of employee


# #### Observations on job experience

# In[24]:


labeled_barplot(data, 'has_job_experience')  ## labeled_barplot for job experience


# #### Observations on job training

# In[25]:


labeled_barplot(data, 'requires_job_training')  ## create labeled_barplot for job training 


# #### Observations on region of employment

# In[27]:


labeled_barplot(data, 'region_of_employment')  ## create labeled_barplot for region of employment


# #### Observations on unit of wage

# In[28]:


labeled_barplot(data, 'unit_of_wage')  ## create labeled_barplot for unit of wage


# #### Observations on case status

# In[29]:


labeled_barplot(data, 'case_status')  ## create labeled_barplot for case status


# ### Bivariate Analysis

# In[30]:


cols_list = data.select_dtypes(include=np.number).columns.tolist()

plt.figure(figsize=(10, 5))
sns.heatmap(
    data[cols_list].corr(), annot=True, vmin=-1, vmax=1, fmt=".2f", cmap="Spectral"
) ## find the correlation between the variables
plt.show()


# **Creating functions that will help us with further analysis.**

# In[31]:


### function to plot distributions wrt target


def distribution_plot_wrt_target(data, predictor, target):

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    target_uniq = data[target].unique()

    axs[0, 0].set_title("Distribution of target for target=" + str(target_uniq[0]))
    sns.histplot(
        data=data[data[target] == target_uniq[0]],
        x=predictor,
        kde=True,
        ax=axs[0, 0],
        color="teal",
        stat="density",
    )

    axs[0, 1].set_title("Distribution of target for target=" + str(target_uniq[1]))
    sns.histplot(
        data=data[data[target] == target_uniq[1]],
        x=predictor,
        kde=True,
        ax=axs[0, 1],
        color="orange",
        stat="density",
    )

    axs[1, 0].set_title("Boxplot w.r.t target")
    sns.boxplot(data=data, x=target, y=predictor, ax=axs[1, 0], palette="gist_rainbow")

    axs[1, 1].set_title("Boxplot (without outliers) w.r.t target")
    sns.boxplot(
        data=data,
        x=target,
        y=predictor,
        ax=axs[1, 1],
        showfliers=False,
        palette="gist_rainbow",
    )

    plt.tight_layout()
    plt.show()


# In[32]:


def stacked_barplot(data, predictor, target):
    """
    Print the category counts and plot a stacked bar chart

    data: dataframe
    predictor: independent variable
    target: target variable
    """
    count = data[predictor].nunique()
    sorter = data[target].value_counts().index[-1]
    tab1 = pd.crosstab(data[predictor], data[target], margins=True).sort_values(
        by=sorter, ascending=False
    )
    print(tab1)
    print("-" * 120)
    tab = pd.crosstab(data[predictor], data[target], normalize="index").sort_values(
        by=sorter, ascending=False
    )
    tab.plot(kind="bar", stacked=True, figsize=(count + 5, 5))
    plt.legend(
        loc="lower left", frameon=False,
    )
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.show()


# #### Those with higher education may want to travel abroad for a well-paid job. Let's find out if education has any impact on visa certification

# In[33]:


stacked_barplot(data, "education_of_employee", "case_status")


# #### Different regions have different requirements of talent having diverse educational backgrounds. Let's analyze it further

# In[34]:


plt.figure(figsize=(10, 5))
sns.heatmap(pd.crosstab(data ['education_of_employee'], data['region_of_employment']),
    annot=True,
    fmt="g",
    cmap="viridis"
) ## plot heatmap for the crosstab between education and region of employment

plt.ylabel("Education")
plt.xlabel("Region")
plt.show()


# #### Let's have a look at the percentage of visa certifications across each region

# In[35]:


stacked_barplot(data, 'region_of_employment', 'case_status') ## plot stacked barplot for region of employment and case status


# #### Lets' similarly check for the continents and find out how the visa status vary across different continents.

# In[36]:


stacked_barplot(data, 'continent', 'case_status') ## plot stacked barplot for continent and case status


# #### Experienced professionals might look abroad for opportunities to improve their lifestyles and career development. Let's see if having work experience has any influence over visa certification 

# In[37]:


stacked_barplot(data, 'has_job_experience', 'case_status') ## plot stacked barplot for job experience and case status


# #### Do the employees who have prior work experience require any job training?

# In[38]:


stacked_barplot(data, 'has_job_experience', 'requires_job_training') ## plot stacked barplot for job experience and requires_job_training


# #### The US government has established a prevailing wage to protect local talent and foreign workers. Let's analyze the data and see if the visa status changes with the prevailing wage

# In[39]:


distribution_plot_wrt_target(data, 'prevailing_wage', 'case_status') ## find distribution of prevailing wage and case status


# #### Checking if the prevailing wage is similar across all the regions of the US

# In[40]:


plt.figure(figsize=(10, 5))
sns.boxplot(data=data, x='region_of_employment', y='prevailing_wage') ## create boxplot for region of employment and prevailing wage
plt.show()


# #### The prevailing wage has different units (Hourly, Weekly, etc). Let's find out if it has any impact on visa applications getting certified.

# In[41]:


stacked_barplot(data, 'unit_of_wage', 'case_status') ## plot stacked barplot for unit of wage and case status


# ## Data Preprocessing

# ### Outlier Check
# 
# - Let's check for outliers in the data.

# In[43]:


# outlier detection using boxplot
numeric_columns = data.select_dtypes(include=np.number).columns.tolist()


plt.figure(figsize=(15, 12))

for i, variable in enumerate(numeric_columns):
    plt.subplot(4,4,i+1)
    plt.boxplot(data[variable], whis = 1.5)
    plt.tight_layout()
    plt.title(variable)## create boxplots for all the numeric columns
plt.show()


# ### Data Preparation for modeling
# 
# - We want to predict which visa will be certified.
# - Before we proceed to build a model, we'll have to encode categorical features.
# - We'll split the data into train and test to be able to evaluate the model that we build on the train data.

# In[44]:


data["case_status"] = data["case_status"].apply(lambda x: 1 if x == "Certified" else 0)

X = data.drop(['case_status'],axis=1) ## drop case status from the data
Y = data["case_status"]


X = pd.get_dummies(X, drop_first = True)  ## create dummies for X 

# Splitting data in train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=.30, random_state=1, stratify=Y) ## split the data into train and test in the ratio 70:30


# In[45]:


print("Shape of Training set : ", X_train.shape)
print("Shape of test set : ", X_test.shape)
print("Percentage of classes in training set:")
print(y_train.value_counts(normalize=True))
print("Percentage of classes in test set:")
print(y_test.value_counts(normalize=True))


# ## Model evaluation criterion

# ### Model can make wrong predictions as:
# 
# 1. Model predicts that the visa application will get certified but in reality, the visa application should get denied.
# 2. Model predicts that the visa application will not get certified but in reality, the visa application should get certified. 
# 
# ### Which case is more important? 
# * Both the cases are important as:
# 
# * If a visa is certified when it had to be denied a wrong employee will get the job position while US citizens will miss the opportunity to work on that position.
# 
# * If a visa is denied when it had to be certified the U.S. will lose a suitable human resource that can contribute to the economy. 
# 
# 
# 
# ### How to reduce the losses?
# 
# * `F1 Score` can be used a the metric for evaluation of the model, greater the F1  score higher are the chances of minimizing False Negatives and False Positives. 
# * We will use balanced class weights so that model focuses equally on both classes.

# **First, let's create functions to calculate different metrics and confusion matrix so that we don't have to use the same code repeatedly for each model.**
# * The model_performance_classification_sklearn function will be used to check the model performance of models. 
# * The confusion_matrix_sklearn function will be used to plot the confusion matrix.

# In[46]:


# defining a function to compute different metrics to check performance of a classification model built using sklearn


def model_performance_classification_sklearn(model, predictors, target):
    """
    Function to compute different metrics to check classification model performance

    model: classifier
    predictors: independent variables
    target: dependent variable
    """

    # predicting using the independent variables
    pred = model.predict(predictors)

    acc = accuracy_score(target, pred)  # to compute Accuracy
    recall = recall_score(target, pred)  # to compute Recall
    precision = precision_score(target, pred)  # to compute Precision
    f1 = f1_score(target, pred)  # to compute F1-score

    # creating a dataframe of metrics
    df_perf = pd.DataFrame(
        {"Accuracy": acc, "Recall": recall, "Precision": precision, "F1": f1,},
        index=[0],
    )

    return df_perf


# In[47]:


def confusion_matrix_sklearn(model, predictors, target):
    """
    To plot the confusion_matrix with percentages

    model: classifier
    predictors: independent variables
    target: dependent variable
    """
    y_pred = model.predict(predictors)
    cm = confusion_matrix(target, y_pred)
    labels = np.asarray(
        [
            ["{0:0.0f}".format(item) + "\n{0:.2%}".format(item / cm.flatten().sum())]
            for item in cm.flatten()
        ]
    ).reshape(2, 2)

    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=labels, fmt="")
    plt.ylabel("True label")
    plt.xlabel("Predicted label")


# ## Decision Tree - Model Building and Hyperparameter Tuning

# ### Decision Tree Model

# In[48]:


model = DecisionTreeClassifier(random_state=1) ## define decision tree classifier with random state = 1
model.fit(X_train, y_train) ## fit decision tree classifier on the train data 


# #### Checking model performance on training set

# In[75]:


confusion_matrix_sklearn(decision_tree_classifier_tuned, X_train, y_train) ## create confusion matrix for train data


# In[78]:


decision_tree_perf_train = model_performance_classification_sklearn(model, X_train, y_train) ## check performance on train data
decision_tree_perf_train


# #### Checking model performance on test set

# In[51]:


confusion_matrix_sklearn(model, X_test, y_test)## create confusion matrix for test data


# In[52]:


decision_tree_perf_test = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data
decision_tree_perf_test


# ### Hyperparameter Tuning - Decision Tree

# In[54]:


# Choose the type of classifier.
dtree_estimator = DecisionTreeClassifier(class_weight="balanced", random_state=1)

# Grid of parameters to choose from
parameters = {
    "max_depth": np.arange(5, 16, 5),
    "min_samples_leaf": [3, 5, 7],
    "max_leaf_nodes": [2, 5],
    "min_impurity_decrease": [0.0001, 0.001],
}

# Type of scoring used to compare parameter combinations
scorer = metrics.make_scorer(metrics.f1_score)

# Run the grid search
grid_obj = GridSearchCV(dtree_estimator, parameters, scoring=scorer, n_jobs=-1) ## run grid search with n_jobs = -1

grid_obj = grid_obj.fit(X_train, y_train) ## fit the grid_obj on the train data

# Set the clf to the best combination of parameters
dtree_estimator = grid_obj.best_estimator_

# Fit the best algorithm to the data.
dtree_estimator.fit(X_train, y_train)


# In[79]:


dtree_estimator_model_train_perf=model_performance_classification_sklearn(dtree_estimator, X_train, y_train)
print('Training performance:\n', dtree_estimator_model_train_perf)## create confusion matrix for train data on tuned estimator


# In[82]:


confusion_matrix_sklearn(model, X_train, y_train)


# In[80]:


dtree_estimator_model_train_perf = model_performance_classification_sklearn(dtree_estimator, X_train, y_train) ## check performance for train data on tuned estimator
dtree_estimator_model_train_perf


# In[57]:


confusion_matrix_sklearn(model, X_test, y_test) ## create confusion matrix for test data on tuned estimator


# In[58]:


dtree_estimator_model_test_perf = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data on tuned estimator
dtree_estimator_model_test_perf


# ## Bagging - Model Building and Hyperparameter Tuning

# ### Bagging Classifier

# In[62]:


bagging_classifier = BaggingClassifier(random_state=1) ## define bagging classifier with random state = 1
bagging_classifier.fit(X_train, y_train) ## fit bagging classifier on the train data


# #### Checking model performance on training set

# In[63]:


confusion_matrix_sklearn(model, X_train, y_train) ## create confusion matrix for train data


# In[64]:


bagging_classifier_model_train_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance on train data
bagging_classifier_model_train_perf


# #### Checking model performance on test set

# In[74]:


confusion_matrix_sklearn(model, X_test, y_test) ## create confusion matrix for test data


# In[66]:


bagging_classifier_model_test_perf = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data
bagging_classifier_model_test_perf


# ### Hyperparameter Tuning - Bagging Classifier

# In[67]:


# Choose the type of classifier.
bagging_estimator_tuned = BaggingClassifier(random_state=1)

# Grid of parameters to choose from
parameters = {
    "max_samples": [0.7, 0.9],
    "max_features": [0.7, 0.9],
    "n_estimators": np.arange(90, 111, 10),
}

# Type of scoring used to compare parameter combinations
acc_scorer = metrics.make_scorer(metrics.f1_score)

# Run the grid search
grid_obj = GridSearchCV(bagging_estimator_tuned, parameters, scoring=acc_scorer, cv=5)## run grid search with cv = 5
grid_obj = grid_obj.fit(X_train, y_train) ##fit the grid_obj on train data

# Set the clf to the best combination of parameters
bagging_estimator_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data.
bagging_estimator_tuned.fit(X_train, y_train)


# #### Checking model performance on training set

# In[69]:


bagging_estimator_tuned_model_train_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance for train data on tuned estimator
bagging_estimator_tuned_model_train_perf


# #### Checking model performance on test set

# In[71]:


confusion_matrix_sklearn(bagging_estimator_tuned, X_test, y_test) ## create confusion matrix for test data on tuned estimator


# In[72]:


bagging_estimator_tuned_model_test_perf = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data on tuned estimator
bagging_estimator_tuned_model_test_perf


# ### Random Forest

# In[85]:


# Fitting the model
rf_estimator = RandomForestClassifier(random_state=1, class_weight='balanced') ## define random forest with random state = 1 and class_weight = balanced
rf_estimator.fit(X_train, y_train) ## fit random forest on the train data


# #### Checking model performance on training set

# In[86]:


rf_estimator_model_train_perf=model_performance_classification_sklearn(rf_estimator, X_train, y_train)
print("Training performance:\n", rf_estimator_model_train_perf)
confusion_matrix_sklearn(rf_estimator, X_train, y_train)## create confusion matrix for train data


# In[87]:


# Calculating different metrics
rf_estimator_model_train_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance on train data
rf_estimator_model_train_perf


# #### Checking model performance on test set

# In[88]:


rf_estimator_model_test_perf=model_performance_classification_sklearn(rf_estimator, X_test, y_test)
print("Test performance:\n", rf_estimator_model_test_perf)
confusion_matrix_sklearn(rf_estimator, X_test, y_test)## create confusion matrix for test data


# In[89]:


rf_estimator_model_test_perf = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data
rf_estimator_model_test_perf


# ### Hyperparameter Tuning - Random Forest

# In[90]:


# Choose the type of classifier.
rf_tuned = RandomForestClassifier(random_state=1, oob_score=True, bootstrap=True)

parameters = {
    "max_depth": list(np.arange(5, 15, 5)),
    "max_features": ["sqrt", "log2"],
    "min_samples_split": [5, 7],
    "n_estimators": np.arange(15, 26, 5),
}

# Type of scoring used to compare parameter combinations
acc_scorer = metrics.make_scorer(metrics.f1_score)

# Run the grid search
grid_obj = GridSearchCV(rf_tuned, parameters, scoring=scorer, cv=5, n_jobs=-1) ## run grid search with cv = 5 and n_jobs = -1
grid_obj = grid_obj.fit(X_train, y_train)## fit the grid_obj on the train data

# Set the clf to the best combination of parameters
rf_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data.
rf_tuned.fit(X_train, y_train)


# #### Checking model performance on training set

# In[ ]:


'_______' ## create confusion matrix for train data on tuned estimator


# In[ ]:


rf_tuned_model_train_perf = model_performance_classification_sklearn('_______') ## check performance for train data on tuned estimator
rf_tuned_model_train_perf


# #### Checking model performance on test set

# In[91]:


rf_tuned_model_train_perf= model_performance_classification_sklearn(rf_tuned, X_train, y_train)
print("Training performance:\n", rf_tuned_model_train_perf)
confusion_matrix_sklearn(rf_tuned, X_train, y_train)## create confusion matrix for test data on tuned estimator


# In[92]:


rf_tuned_model_test_perf = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data on tuned estimator
rf_tuned_model_test_perf


# ## Boosting - Model Building and Hyperparameter Tuning

# ### AdaBoost Classifier

# In[93]:


ab_classifier = AdaBoostClassifier(random_state=1) ## define AdaBoost Classifier with random state = 1
ab_classifier.fit(X_train, y_train) ## fit AdaBoost Classifier on the train data


# #### Checking model performance on training set

# In[94]:


ab_classifier_model_train_perf=model_performance_classification_sklearn(ab_classifier, X_train, y_train)
print("Training performance: \n", ab_classifier_model_train_perf)
confusion_matrix_sklearn(ab_classifier, X_train, y_train)## confusion matrix for train data


# In[95]:


ab_classifier_model_train_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance on train data
ab_classifier_model_train_perf


# #### Checking model performance on test set

# In[98]:


ab_classifier_model_test_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance for test data
ab_classifier_model_test_perf


# In[99]:


ab_classifier_model_test_perf_model=model_performance_classification_sklearn(ab_classifier, X_test, y_test)
print("Test performance:\n", ab_classifier_model_test_perf)
confusion_matrix_sklearn(ab_classifier, X_test, y_test)


# In[100]:


ab_classifier_model_test_perf=model_performance_classification_sklearn(model, X_test, y_test)
ab_classifier_model_test_perf


# ### Hyperparameter Tuning - AdaBoost Classifier

# In[101]:


# Choose the type of classifier.
abc_tuned = AdaBoostClassifier(random_state=1)

# Grid of parameters to choose from
parameters = {
    # Let's try different max_depth for base_estimator
    "base_estimator": [
        DecisionTreeClassifier(max_depth=1, class_weight="balanced", random_state=1),
        DecisionTreeClassifier(max_depth=2, class_weight="balanced", random_state=1),
    ],
    "n_estimators": np.arange(80, 101, 10),
    "learning_rate": np.arange(0.1, 0.4, 0.1),
}

# Type of scoring used to compare parameter  combinations
acc_scorer = metrics.make_scorer(metrics.f1_score)

# Run the grid search
grid_obj = GridSearchCV(abc_tuned, parameters, scoring=scorer,cv=5) ## run grid search with cv = 5
grid_obj = grid_obj.fit(X_train, y_train) ## fit the grid_obj on train data

# Set the clf to the best combination of parameters
abc_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data.
abc_tuned.fit(X_train, y_train)


# #### Checking model performance on training set

# In[103]:


abc_tuned_model_train_perf=model_performance_classification_sklearn(abc_tuned, X_train, y_train)
print("Training performance:\n", abc_tuned_model_train_perf)
confusion_matrix_sklearn(abc_tuned, X_train, y_train)## create confusion matrix for train data on tuned estimator


# In[104]:


abc_tuned_model_train_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance for train data on tuned estimator
abc_tuned_model_train_perf


# #### Checking model performance on test set

# In[105]:


abc_tuned_model_test_perf=model_performance_classification_sklearn(abc_tuned, X_test, y_test)
print("Test performance:\n", abc_tuned_model_test_perf)
confusion_matrix_sklearn(abc_tuned, X_test, y_test)## create confusion matrix for test data on tuned estimator


# In[106]:


abc_tuned_model_test_perf = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data on tuned estimator
abc_tuned_model_test_perf


# ### Gradient Boosting Classifier

# In[107]:


gb_classifier = GradientBoostingClassifier(random_state=1) ## define Gradient Boosting Classifier with random state = 1
gb_classifier.fit(X_train, y_train) ## fit Gradient Boosting Classifier on the train data


# #### Checking model performance on training set

# In[108]:


gb_classifier_model_train_perf=model_performance_classification_sklearn(ab_classifier, X_train, y_train)
print("Training performance:\n", gb_classifier_model_train_perf)
confusion_matrix_sklearn(gb_classifier, X_train, y_train)## create confusion matrix for train data


# In[109]:


gb_classifier_model_train_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance on train data
gb_classifier_model_train_perf


# #### Checking model performance on test set

# In[110]:


gb_classifier_model_test_perf=model_performance_classification_sklearn(ab_classifier, X_test, y_test)
print("Test performance:\n", gb_classifier_model_test_perf)
confusion_matrix_sklearn(gb_classifier, X_test, y_test)## create confusion matrix for test data


# In[111]:


gb_classifier_model_test_perf = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data
gb_classifier_model_test_perf


# ### Hyperparameter Tuning - Gradient Boosting Classifier

# In[113]:


# Choose the type of classifier.
gbc_tuned = GradientBoostingClassifier(
    init=AdaBoostClassifier(random_state=1), random_state=1
)

# Grid of parameters to choose from
parameters = {
    "n_estimators": [200, 250],
    "subsample": [0.9, 1],
    "max_features": [0.8, 0.9],
    "learning_rate": np.arange(0.1, 0.21, 0.1),
}

# Type of scoring used to compare parameter combinations
acc_scorer = metrics.make_scorer(metrics.f1_score)

# Run the grid search
grid_obj = GridSearchCV(gbc_tuned, parameters, scoring=scorer, cv=5, n_jobs=-1) ## run grid search with cv = 5
grid_obj = grid_obj.fit(X_train, y_train) ## the grid_obj on train data

# Set the clf to the best combination of parameters
gbc_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data.
gbc_tuned.fit(X_train, y_train)


# #### Checking model performance on training set

# In[114]:


gbc_tuned_model_train_perf = model_performance_classification_sklearn(gbc_tuned, X_train, y_train)
print("Training performance:\n", gbc_tuned_model_train_perf)
confusion_matrix_sklearn(gbc_tuned, X_train, y_train)## create confusion matrix for train data on tuned estimator


# In[115]:


gbc_tuned_model_train_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance for train data on tuned estimator
gbc_tuned_model_train_perf


# #### Checking model performance on test set

# In[116]:


gbc_tuned_model_test_perf=model_performance_classification_sklearn(gbc_tuned, X_test, y_test)
print("Test performance:\n", gbc_tuned_model_test_perf)
confusion_matrix_sklearn(gbc_tuned, X_test, y_test)## create confusion matrix for test data on tuned estimator


# In[117]:


gbc_tuned_model_test_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance for test data on tuned estimator
gbc_tuned_model_test_perf


# ### Note - You can choose **not to build** XGBoost if you have any installation issues

# ### XGBoost Classifier

# In[118]:


xgb_classifier = XGBClassifier(random_state=1, eval_metric='logloss') ## define XGBoost Classifier with random state = 1 and eval_metric="logloss"
xgb_classifier.fit(X_train, y_train) ## fit XGBoost Classifier on the train data


# #### Checking model performance on training set

# In[119]:


xgb_classifier_model_train_perf=model_performance_classification_sklearn(xgb_classifier, X_train, y_train)
print("Training performance:\n", xgb_classifier_model_train_perf)
confusion_matrix_sklearn(xgb_classifier, X_train, y_train)## create confusion matrix for train data


# In[120]:


xgb_classifier_model_train_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance on train data
xgb_classifier_model_train_perf


# #### Checking model performance on test set

# In[121]:


xgb_classifier_model_test_perf=model_performance_classification_sklearn(xgb_classifier, X_test, y_test)
print("Test performance:\n", xgb_classifier_model_test_perf)
confusion_matrix_sklearn(xgb_classifier, X_test, y_test)## create confusion matrix for test data


# In[122]:


xgb_classifier_model_test_perf = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data
xgb_classifier_model_test_perf


# ### Hyperparameter Tuning - XGBoost Classifier

# In[126]:


get_ipython().system('pip install xgboost')


# In[125]:


# Choose the type of classifier.
xgb_tuned = XGBClassifier(random_state=1, eval_metric="logloss")

# Grid of parameters to choose from
parameters = {
    "n_estimators": np.arange(150, 250, 50),
    "scale_pos_weight": [1, 2],
    "subsample": [0.9, 1],
    "learning_rate": np.arange(0.1, 0.21, 0.1),
    "gamma": [3, 5],
    "colsample_bytree": [0.8, 0.9],
    "colsample_bylevel": [ 0.9, 1],
}

# Type of scoring used to compare parameter combinations
acc_scorer = metrics.make_scorer(metrics.f1_score)

# Run the grid search
grid_obj = GridSearchCV(xgb_tuned, parameters, scoring=scorer, cv=5) ## run grid search with cv = 5
grid_obj = grid_obj.fit(X_train, y_train) ## fit the grid_obj on train data

# Set the clf to the best combination of parameters
xgb_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data.
xgb_tuned.fit(X_train, y_train)


# #### Checking model performance on training set

# In[124]:


xgb_tuned_model_train_perf = model_performance_classification_sklearn(xgb_tuned, X_train, y_train)
print("Training performance:\n", xgb_tuned_model_train_perf)
confusion_matrix_sklearn(xgb_tuned, X_train, y_train)## create confusion matrix for train data on tuned estimator


# In[127]:


xgb_tuned_model_train_perf = model_performance_classification_sklearn(model, X_train, y_train) ## check performance for train data on tuned estimator
xgb_tuned_model_train_perf


# #### Checking model performance on test set

# In[135]:


xgb_tuned_model_test_perf = model_performance_classification_sklearn(xgb_tuned, X_test, y_test)
print("Test performance:\n", xgb_tuned_model_test_perf)
confusion_matrix_sklearn(xgb_tuned, X_test, y_test)## create confusion matrix for test data on tuned estimator


# In[129]:


xgb_tuned_model_test_perf = model_performance_classification_sklearn(model, X_test, y_test) ## check performance for test data on tuned estimator
xgb_tuned_model_test_perf


# ## Stacking Classifier

# In[130]:


estimators = [
    ("AdaBoost", ab_classifier),
    ("Gradient Boosting", gbc_tuned),
    ("Random Forest", rf_tuned),
]

final_estimator = xgb_tuned

stacking_classifier = StackingClassifier(
estimators=estimators, final_estimator=final_estimator) ## define Stacking Classifier

stacking_classifier.fit(X_train, y_train) ## fit Stacking Classifier on the train data


# ### Checking model performance on training set

# In[131]:


confusion_matrix_sklearn(stacking_classifier, X_train, y_train) ## create confusion matrix for train data


# In[132]:


stacking_classifier_model_train_perf = model_performance_classification_sklearn(stacking_classifier, X_train, y_train) ## check performance on train data
stacking_classifier_model_train_perf


# ### Checking model performance on test set

# In[136]:


confusion_matrix_sklearn(stacking_classifier, X_test, y_test) ## create confusion matrix for test data


# In[133]:


stacking_classifier_model_test_perf = model_performance_classification_sklearn(stacking_classifier, X_test, y_test) ## check performance for test data
stacking_classifier_model_test_perf


# ## Model Performance Comparison and Final Model Selection

# In[137]:


# training performance comparison

models_train_comp_df = pd.concat(
    [
        decision_tree_perf_train.T,
        dtree_estimator_model_train_perf.T,
        bagging_classifier_model_train_perf.T,
        bagging_estimator_tuned_model_train_perf.T,
        rf_estimator_model_train_perf.T,
        rf_tuned_model_train_perf.T,
        ab_classifier_model_train_perf.T,
        abc_tuned_model_train_perf.T,
        gb_classifier_model_train_perf.T,
        gbc_tuned_model_train_perf.T,
        xgb_classifier_model_train_perf.T,
        xgb_tuned_model_train_perf.T,
        stacking_classifier_model_train_perf.T,
    ],
    axis=1,
)
models_train_comp_df.columns = [
    "Decision Tree",
    "Tuned Decision Tree",
    "Bagging Classifier",
    "Tuned Bagging Classifier",
    "Random Forest",
    "Tuned Random Forest",
    "Adaboost Classifier",
    "Tuned Adaboost Classifier",
    "Gradient Boost Classifier",
    "Tuned Gradient Boost Classifier",
    "XGBoost Classifier",
    "XGBoost Classifier Tuned",
    "Stacking Classifier",
]
print("Training performance comparison:")
models_train_comp_df


# In[144]:


models_test_comp_df = pd.concat(
    [
        decision_tree_perf_test.T,
        dtree_estimator_model_test_perf.T,
        bagging_classifier_model_test_perf.T,
        bagging_estimator_tuned_model_test_perf.T,
        rf_estimator_model_test_perf.T,
        rf_tuned_model_test_perf.T,
        ab_classifier_model_test_perf.T,
        abc_tuned_model_test_perf.T,
        gb_classifier_model_test_perf.T,
        gbc_tuned_model_test_perf.T,
        xgb_classifier_model_test_perf.T,
        xgb_tuned_model_test_perf.T,
        stacking_classifier_model_test_perf.T,
    ],
    axis=1,
)
models_test_comp_df.columns = [
    "Decision Tree",
    "Tuned Decision Tree",
    "Bagging Classifier",
    "Tuned Bagging Classifier",
    "Random Forest",
    "Tuned Random Forest",
    "Adaboost Classifier",
    "Tuned Adaboost Classifier",
    "Gradient Boost Classifier",
    "Tuned Gradient Boost Classifier",
    "XGBoost Classifier",
    "XGBoost Classifier Tuned",
    "Stacking Classifier",
]
print("Test performance comparison:")
models_test_comp_df


# ### Important features of the final model

# In[145]:


feature_names = X_train.columns
importances = gb_classifier.feature_importances_
indices = np.argsort(importances)

plt.figure(figsize=(12, 12))
plt.title("Feature Importances")
plt.barh(range(len(indices)), importances[indices], color="violet", align="center")
plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
plt.xlabel("Relative Importance")
plt.show()


# ## Business Insights and Recommendations

# - 
# 

# ___
