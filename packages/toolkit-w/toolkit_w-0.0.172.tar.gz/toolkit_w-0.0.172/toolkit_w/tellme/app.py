import streamlit as st
from dash import MultiApp
from apps import summary, orders, customers,traffic,discounts,churn,product_rec,products # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Summary stats", summary.app)
app.add_app("Orders data analysis", orders.app)
app.add_app("Customers data analysis", customers.app)
app.add_app('Paid traffic analysis', traffic.app)
app.add_app('Discount Analysis', discounts.app)
app.add_app('Customer churn', churn.app)
app.add_app('Product Recommendation', product_rec.app)
app.add_app('Products Analysis', products.app)
# The main app
app.run()