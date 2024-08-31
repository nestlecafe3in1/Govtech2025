# Govtech2025

The following `python` program  extracts and analyzes restaurant data from Zomato. It processes and examines restaurant ratings, events, and other relevant data to identify top-rated restaurants and noteworthy past events, providing valuable insights for curating a travel food experience.


## Pre-requisites

* Python >= 3

## Required Packages

Before running the program, ensure that you have the necessary Python packages installed. You can install them using `pip` with the following command:

```commandline
$ pip install pandas numpy requests
```
## How to Run

Once you have a python environment setup, you can navigate to the project directory and execute this command:

```commandline
$ python Main.py
```
## Output results example

Successful run with python `Main.py` will output the following:
```plaintext
Restaurant Data exported successfully to output/restaurants.csv
**********************************************************************
Restaurant Data exported successfully to output/restaurant_events.csv
**********************************************************************
Threshold for the different rating text:
Rating Text  min  max
Poor         2.2  2.2
Average      2.5  3.4
Good         3.5  3.9
Very Good    4.0  4.4
Excellent    4.5  4.9
```


