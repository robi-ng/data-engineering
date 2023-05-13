# Data Pipelines for E-commerce Membership

## Overview

This project runs data pipeline of e-commerce membership data by reading csv files located in `raw-data` folder.

## How to run

### 1. Install requirements

Ensure that python environment with pip is available. Run `pip install -r requirements.txt` to install the dependencies.

### 2. Place raw csv data files in the correct folder

Ensure raw csv data files are placed in the `raw-data` folder.

The following sample datasets are available as example:

- `raw-data/applications_dataset_1.csv`

- `raw-data/applications_dataset_2.csv`

### 3. Run the python script

Run `python process_raw_membership.py` to process the raw data files.

By default, it will only run raw data files modified in the last one hour. Specify `-a` option to process all raw data files.

Schedule the script via cron to process it hourly, e.g.
```
0 * * * * python /full/path/to/data-pipelines/process_raw_membership.py >> /full/path/to/data-pipelines/process_raw_membership.log 2>&1
```

### 3. Output files are generated

Output files are generated in `processed-data` folder, which is further separated by `successful` folder for successful applications, and `unsuccessful` folder unsuccessful applications.

The following sample output files are available as example:

- `processed-data/successful/successful_applications_2023-05-13T15:09:51.747242+08:00.csv`

- `processed-data/unsuccessful/unsuccessful_applications_2023-05-13T15:09:51.747242+08:00.csv`
