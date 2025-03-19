import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from datetime import timedelta
import pandas as pd
from dateutil.relativedelta import relativedelta

def exponential_interpolation(data):
  # Sort data by date
  data_sorted = sorted(data, key=lambda x: x['date'])
  
  try:
    dates = [d['date'] for d in data_sorted]
    values = np.array([d['value'] for d in data_sorted])
    
    first_date = dates[0]
    numeric_dates = np.array([(d.year - first_date.year) * 12 + (d.month - first_date.month) for d in dates])
    
    log_values = np.log(values)
    slope, intercept, _, _, _ = linregress(numeric_dates, log_values)
      
  except Exception as e:
    st.error(f'Error processing data: {str(e)}')
    return

  a = np.exp(intercept)
  b = slope

  last_date = dates[-1]
  future_months = 6
  extended_date = last_date + relativedelta(months=future_months)
  
  fit_start = first_date
  fit_end = extended_date
  date_range = pd.date_range(start=fit_start, end=fit_end, periods=5)
  
  numeric_fit = np.array([(d.year - first_date.year) * 12 + (d.month - first_date.month) for d in date_range])
  
  y_fit = a * np.exp(b * numeric_fit)

  fig, ax = plt.subplots()
  
  ax.scatter(dates, values, label="Dados originais", zorder=3, s=50)
  
  ax.plot(date_range, y_fit, 'r-', label=f'Interpolação: y = {a:.2f}e$^{{{b:.2f}x}}$')
  
  future_dates = [last_date + relativedelta(months=i) for i in range(1, future_months+1)]
  future_values = a * np.exp(b * (numeric_dates[-1] + np.arange(1, future_months+1)))
  
  ax.scatter(future_dates, future_values, color='orange', edgecolors='darkred', label='Valores Projetados', zorder=3)
  
  ax.axvline(x=last_date, color='gray', linestyle='--', linewidth=1)
  ax.text(last_date + timedelta(days=5), np.min(values), 'Extrapolação', rotation=90, va='bottom')
  
  ax.set_xlabel('Data')
  ax.set_ylabel('Valor')
  ax.grid(True, linestyle='--', alpha=0.7)
  ax.legend()
  
  plt.xticks(rotation=45)
  ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b-%Y'))
  
  st.pyplot(fig)

  formatted_future_values = []
  for value in future_values:
    formatted_future_values.append("R$ " + str(np.round(value, 2)))

  st.subheader("Projeções Futuras")
  projection_data = {
      "Data": [d.strftime('%b-%Y') for d in future_dates],
      "Valor Projetado": formatted_future_values
  }
  st.dataframe(pd.DataFrame(projection_data))
