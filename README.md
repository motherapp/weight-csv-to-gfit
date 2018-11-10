# google-fit-data
Load bulk weight/steps data to a Google Fit account

## Download and installation
```
git clone https://github.com/motherapp/weight-csv-to-gfit.git
cd weight-csv-to-gfit
virtualenv -p /usr/bin/python2.7 venv
pip install -r requirements.txt
```

## Export weight data to Google Fit
```
python weight/import_weight_to_gfit.py
```

## Export steps data to Google Fit
```
python steps/import_steps_to_gfit.py
```
