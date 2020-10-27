import pandas as pd
import numpy as np

reference_data = 2019;
recidiviz_3_year_rate = 0.391

population_data = pd.DataFrame({
    'year': [-2, -1, 0]
})

historical_data_2019 = pd.read_csv('2019.csv')
print(historical_data_2019)
