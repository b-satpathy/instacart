owner='Bishwa Satpathy'

#import libraries
import pandas as pd
import operator

#read the data

# aisles
aisles = pd.read_csv('aisles.csv')
print('Total aisles: {}'.format(aisles.shape[0]))
#print(aisles.head())

# departments
departments = pd.read_csv('departments.csv')
print('Total departments: {}'.format(departments.shape[0]))
#print(departments.head())

# products
products = pd.read_csv('products.csv')
print('Total products: {}'.format(products.shape[0]))
#print(products.head())

# inner join aisles, departments and products
inventory = pd.merge(left=pd.merge(left=products, right=aisles, on='aisle_id', how='inner'), right=departments, on='department_id', how='inner')
print('Total inventory: {}'.format(inventory.shape[0]))
print(inventory.head())
