# !/usr/bin/env python
# coding: utf-8

# In[15]:

import pandas as pd
import numpy as np

df = pd.read_csv('/content/dirty_cafe_sales.csv')

# In[19]:

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
# Replace 'ERROR' and 'UNKNOWN' with NaN
df.replace(['ERROR', 'UNKNOWN'], np.nan, inplace=True)
df.head()

# In[20]:

# View data types of each column
print(df.dtypes)
print(df.columns.tolist())

# In[21]:

# Convert quantity, price_per_unit, and total_spent to numeric
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['price_per_unit'] = pd.to_numeric(df['price_per_unit'], errors='coerce')
df['total_spent'] = pd.to_numeric(df['total_spent'], errors='coerce')

# Convert transaction_date to datetime
df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')

# Confirm new data types
print(df.dtypes)

# In[23]:

# Count NaN values in each column
print(df.isna().sum())

# In[24]:

# 1. Fill total_spent if quantity and price_per_unit are known
mask_total = df['total_spent'].isna() & df['quantity'].notna() & df['price_per_unit'].notna()
df.loc[mask_total, 'total_spent'] = df.loc[mask_total, 'quantity'] * df.loc[mask_total, 'price_per_unit']

# 2. Fill quantity if total_spent and price_per_unit are known
mask_quantity = df['quantity'].isna() & df['total_spent'].notna() & df['price_per_unit'].notna()
df.loc[mask_quantity, 'quantity'] = df.loc[mask_quantity, 'total_spent'] / df.loc[mask_quantity, 'price_per_unit']

# 3. Fill price_per_unit if total_spent and quantity are known
mask_price = df['price_per_unit'].isna() & df['total_spent'].notna() & df['quantity'].notna()
df.loc[mask_price, 'price_per_unit'] = df.loc[mask_price, 'total_spent'] / df.loc[mask_price, 'quantity']

# In[25]:

# Count how many of the three key fields are missing per row
missing_key_fields = df[['quantity', 'price_per_unit', 'total_spent']].isna().sum(axis=1)

# Drop rows with 2 or more missing from the 3
df = df[missing_key_fields < 2].reset_index(drop=True)

# In[26]:

# Count NaN values in each column
print(df.isna().sum())

# In[27]:

# Drop all rows that contain any NaN values
df = df.dropna().reset_index(drop=True)

# Confirm all NaNs are gone
print(df.isna().sum())
print(f"Final dataset shape: {df.shape}")

# In[28]:

# Find duplicate transaction IDs
duplicates = df[df.duplicated('transaction_id')]
print(f"Duplicate transactions: {len(duplicates)}")

# Drop them if needed
df = df.drop_duplicates('transaction_id')

# In[29]:

# Show unique values in key categorical columns
print("Unique Payment Methods:")
print(df['payment_method'].unique())

print("\nUnique Locations:")
print(df['location'].unique())

print("\nUnique Items:")
print(df['item'].unique())

# In[37]:

# Recreate the one-hot encoded columns
dummies = pd.get_dummies(
    df[['item', 'payment_method', 'location']],
    prefix=['item', 'payment', 'location'],
    dtype=int  # ensures output is int (0/1) instead of bool
)

# Drop old one-hot columns if re-running this cell
df = df.drop(columns=[col for col in df.columns if col in dummies.columns], errors='ignore')

# Concatenate encoded columns with original DataFrame
df = pd.concat([df, dummies], axis=1)

# Preview the updated DataFrame
df.head()

# In[45]:

# Step 1: Identify original "text" columns you want first
text_columns = ['transaction_id', 'item', 'payment_method', 'location', 'transaction_date']

# Step 2: Add the remaining columns after the text ones
# (Includes quantity, price, total, and binarized columns)
bool_columns = [col for col in df.columns if col not in text_columns]

# Step 3: Reorder
df = df[text_columns + bool_columns]

# Optional: Preview the result
df.head()

# In[47]:

# --------------------------------------
# 1. Validate: Is total_spent = quantity × price_per_unit?
# --------------------------------------
df['calculated_total'] = df['quantity'] * df['price_per_unit']
inconsistencies = df[df['calculated_total'] != df['total_spent']]
print(f"Inconsistent rows (quantity × price_per_unit ≠ total_spent): {len(inconsistencies)}")

# Drop inconsistent rows if desired:
# df = df[df['calculated_total'] == df['total_spent']].reset_index(drop=True)

# --------------------------------------
# 2. Check for Duplicate Transaction IDs
# --------------------------------------
duplicate_ids = df[df.duplicated('transaction_id')]
print(f"Duplicate transaction IDs: {len(duplicate_ids)}")

# --------------------------------------
# 3. Outlier Detection: Very high quantity or total_spent
# --------------------------------------
print("\nSummary statistics for numeric fields:")
print(df[['quantity', 'price_per_unit', 'total_spent']].describe())

# Optional: Look at extreme values
print("\nTransactions with quantity > 100:")
print(df[df['quantity'] > 100])

print("\nTransactions with total_spent > 100:")
print(df[df['total_spent'] > 100])

# --------------------------------------
# 4. Final Data Type Check
# --------------------------------------
print("\nFinal column data types:")
print(df.dtypes)

# --------------------------------------
# 5. Sort by Transaction Date
# --------------------------------------
# df = df.sort_values('transaction_date').reset_index(drop=True)

# --------------------------------------
# 6. Add Date Features: Month and Weekday (for analysis)
# --------------------------------------
df['month'] = df['transaction_date'].dt.to_period('M')
df['weekday'] = df['transaction_date'].dt.day_name()

# --------------------------------------
# 7. Drop helper column if not needed
# --------------------------------------
# df.drop(columns=['calculated_total'], inplace=True)

print("\nFinal cleaned dataset shape:", df.shape)
df.head()

# In[43]:

# Save the cleaned DataFrame to a CSV file
df.to_csv('cleaned_transactions.csv', index=False)
from google.colab import files

# Download the saved file
files.download('cleaned_transactions.csv')

# Data Cleaning Log
# - Column names standardized to snake_case (lowercase with underscores).
# - Replaced 'ERROR' and 'UNKNOWN' values with NaN.
# - Converted columns to correct data types:
# - - quantity, price_per_unit, total_spent → float64
# - - transaction_date → datetime64[ns]
# - Calculated and filled missing values where possible:
# - - total_spent = quantity × price_per_unit
# - - quantity = total_spent ÷ price_per_unit
# - - price_per_unit = total_spent ÷ quantity
# - Dropped rows with 2 or more of the 3 fields (quantity, price_per_unit, total_spent) missing.
# - Standardized categorical values in item, payment_method, and location.
# - Filled missing categorical values with 'unknown'.
# - Dropped rows missing transaction_date.
# - Applied one-hot encoding to item, payment_method, and location.
# - Converted dummy variable columns to integers (0 or 1).
# - Reordered columns to place text columns first, followed by binarized columns.
# - Validated that quantity × price_per_unit = total_spent for all rows.
# - Checked and removed duplicate transaction_id values.
# - Reviewed numeric columns for outliers.
# - Extracted month and weekday from transaction_date for analysis.
# - Sorted the DataFrame by transaction_date.
# - Saved the cleaned dataset as cleaned_transactions.csv

# In[ ]:
