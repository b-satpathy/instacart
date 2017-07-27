owner='Bishwa Satpathy'
# a user could have multiple orders and one order could have multiple products.
# all user history is present in order_products_prior dataset. The latest order of users are either present in train dataset or in test dataset
# we need to predict all the products that the user will order (order id present in test dataset)

#import libraries
import pandas as pd
import operator
import csv

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
products = pd.read_csv('products.csv', engine='c')
print('Total products: {}'.format(products.shape[0]))
#print(products.head())

# inner join aisles, departments and products
inventory = pd.merge(left=pd.merge(left=products, right=aisles, on='aisle_id', how='inner'), right=departments, on='department_id', how='inner')
print('Total inventory: {}'.format(inventory.shape[0]))
#print(inventory.head())


# load training dataset
train = pd.read_csv('order_products__train.csv')
print('Total train: {}'.format(train.shape[0]))
#print(train.head())

# load prior dataset
prior = pd.read_csv('order_products__prior.csv')
print('Total prior: {}'.format(prior.shape[0]))
#print(prior.head())

# load orders dataset
orders = pd.read_csv('orders.csv')
print('Total orders: {}'.format(orders.shape[0]))
#print(orders.head())

# create test dataset from orders dataset
test_orders = orders[orders.eval_set == 'test']
print('Total test_orders: {}'.format(test_orders.shape[0]))

# 1st submission - repeat the last re-ordered products
test_history = orders[(orders.user_id.isin(test_orders.user_id))]
test_history = test_history[test_history['eval_set'] == 'prior']

# find the max order_number for each user
last_orders = test_history.groupby('user_id')['order_number'].max()
print('Total last_orders: {}'.format(last_orders.shape[0]))

# join test history and last order to get the last order for each customer
last_order_details = pd.merge(left=test_history, right=last_orders.reset_index(), how='inner', on=['user_id', 'order_number'])

print('Total last_orders_details: {}'.format(last_order_details.shape[0]))
last_reordered_products = pd.merge(left=last_order_details, right=prior[prior['reordered'] == 1], how='inner', on='order_id')
submission_file = pd.merge(left=test_orders[['order_id', 'user_id']], right=last_reordered_products[['order_id', 'user_id', 'product_id']], how='left', on='user_id').fillna(-1)
submission_file = submission_file[['order_id_x','product_id']]
submission_file = submission_file.astype(int)
submission_file = submission_file.groupby('order_id_x')['product_id'].apply(lambda x: ' '.join([str(e) for e in set(x)])).reset_index()
submission_file = submission_file.replace(to_replace='-1', value='None')
submission_file.columns = ['order_id', 'products']
print('Total submission_file: {}'.format(submission_file.shape[0]))
print(submission_file.head())
submission_file.to_csv('submission_file_last_reordered.csv', index=False,quoting=csv.QUOTE_NONNUMERIC)
