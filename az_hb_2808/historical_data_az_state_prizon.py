import pandas as pd
import numpy as np

reference_data = 2020;
recidiviz_3_year_rate = 0.391

historical_data_2019 = pd.read_csv('2019.csv')
historical_data_2018 = pd.read_csv('2018.csv')
historical_data_2017 = pd.read_csv('2017.csv')

crimes = historical_data_2019.crime.to_list()

is_violent_map = {
    'arson': True,
    'assault': True,
    'auto_theft': False,
    'burglary_or_criminal_trespass': True, # only certain kinds of burglary
    'child_or_adult_abuse': True, # only child abuse would be violent?
    'child_molestation': True,
    'criminal_damage': False,
    'domestic_violence': False,
    'drug_possession': False,
    'drug_trafficking': False,
    'dui': False,
    'escape': False,
    'forgery': False,
    'fraud': False,
    'identity_theft': False,
    'kidnapping': True,
    'manslaughter_or_neg_homicide': True,
    'murder': True,
    'other': False,
    'rape_or_sexual_assault': True,
    'robbery': True,
    'sex_offense': False,
    'theft': False,
    'trafficking_in_stolen_property': False,
    'weapons_offense': True,
}

def get_field_for_crime(df, field, crime):
    return df.loc[df['crime'] == crime][field].to_list()[0]

def get_yearly_fields_for_crime(field, crime):
    return [
        get_field_for_crime(historical_data_2017, field, crime),
        get_field_for_crime(historical_data_2018, field, crime),
        get_field_for_crime(historical_data_2019, field, crime)
    ]

population_by_crime = {crime: get_yearly_fields_for_crime('total', crime) for crime in crimes}
population_data = pd.DataFrame({
    'year': [-3, -2, -1],
    **population_by_crime
});

admissions_by_crime = {crime: get_yearly_fields_for_crime('admissions', crime) for crime in crimes}
admissions_data = pd.DataFrame({
    'year': [-3, -2, -1],
    **admissions_by_crime
});

releases_by_crime = {crime: get_yearly_fields_for_crime('releases', crime) for crime in crimes}
releases_data = pd.DataFrame({
    'year': [-3, -2, -1],
    **releases_by_crime
});

transitions_data = pd.DataFrame(
    columns=['compartment', 'outflow_to', 'total_population', 'compartment_duration', 'crime_type', 'is_violent'])
outflows_data = pd.DataFrame(
    columns=['compartment', 'outflow_to', 'total_population', 'time_step', 'crime_type', 'is_violent'])
total_population_data = pd.DataFrame(
    columns=['compartment', 'total_population', 'time_step', 'crime_type', 'is_violent'])

# TRANSITIONS TABLE

# OUTFLOWS TABLE
for crime in crimes:
    admissions_outflows_data = pd.DataFrame({
        'compartment': ['pre-trial' for year in admissions_data.year],
        'outflow_to': ['prison' for year in admissions_data.year],
        'total_population': admissions_data[crime].to_list(),
        'time_step':admissions_data.year.to_list(),
        'crime_type': [crime for year in admissions_data.year],
        'is_violent': [is_violent_map[crime] for year in admissions_data.year],
    })
    prison_outflows_data = pd.DataFrame({
        'compartment': ['prison' for year in releases_data.year],
        'outflow_to': ['release' for year in releases_data.year],
        'total_population': releases_data[crime].to_list(),
        'time_step': releases_data.year.to_list(),
        'crime_type': [crime for year in releases_data.year],
        'is_violent': [is_violent_map[crime] for year in releases_data.year],
    })
    outflows_data = pd.concat([outflows_data, admissions_outflows_data, prison_outflows_data])

# TOTAL POPULATION TABLE
for crime in crimes:
    crime_total_population = pd.DataFrame({
        'compartment': ['prison' for year in population_data.year],
        'total_population': population_data[crime].to_list(),
        'time_step': population_data.year.to_list(),
        'crime_type': [crime for year in population_data.year],
        'is_violent': [is_violent_map[crime] for year in population_data.year],
    })
    total_population_data = pd.concat([total_population_data, crime_total_population])

