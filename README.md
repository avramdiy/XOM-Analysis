# TRG Week 36

## $XOM

- XOM (Exxon Mobil Corporation) is a leading multinational oil and gas company engaged in exploration, production, and refining of petroleum products.

- https://www.kaggle.com/borismarjanovic/datasets

### 1st Commit

- Load data through data.py to analyze & clean HTML dataframe.

### 2nd Commit

- Past code did not generate an HTML link. Edited parsing logic.

- Dropped OpenInt column.

- Data starts from 1970-01-02 and ends with 2017-11-10.

### 3rd Commit

- Implemented logic to split the cleaned DataFrame by decade (1970s, 1980s, 1990s, 2000s, 2010s).


- Added decade-wise summary statistics and displayed each decade’s data and stats on the Flask web interface.

### 4th Commit

- Adjusted each split decade dataframe to load the first 5 rows and provide a visualization for each dataframe.

### 5th Commit