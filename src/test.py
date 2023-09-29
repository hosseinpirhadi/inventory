# import requests

# response = requests.post(
#                         "http://localhost:8000/token",
#                         data={"username": "ali", "password": "ali"},
#                         )
# print(response.json()["access_token"])


# import requests

# url = "http://localhost:8000/product"  # Replace with the URL you want to send the request to
# bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGkiLCJleHAiOjE2OTU5MTg4Mjl9.KSYZ7JP6jN8sjFsMDrU5oEw_eFQi-T0kEN8_e6fh36Y"  # Replace with your actual bearer token

# headers = {
#     "Authorization": f"Bearer {bearer_token}",
#     "Content-Type": "application/json"  # Adjust content type if needed
# }

# # Make a GET request with the specified headers
# response = requests.get(url, headers=headers)

# # Check the response
# if response.status_code == 200:
#     # Successful response
#     print("Request successful")
#     print("Response content:", response.json())
# else:
#     print("Request failed with status code:", response.status_code)
#     print("Response content:", response.text)

# from sqlalchemy import inspect
# from Repository.database import ENGINE, BASE
# # from Repository.models.warehouse import Warehouse
# # from Repository.models.product_count import ProductCount
# # from Repository.models.product import Product
# # from Repository.models.person import Person
# from Repository.models.inventory import Inventory

# # print(BASE.metadata.tables)
# BASE.metadata.create_all(bind=ENGINE)

# print("Tables created successfully.")

# inspector = inspect(ENGINE)


# print(inspector.has_table('Product'))
# print(inspector.has_table('Warehouse'))
# print(inspector.has_table('Inventory'))
# print(inspector.has_table('ProductCount'))
# print(inspector.has_table('Person'))

# # columns_product = inspector.get_columns('Product')
# # columns_warehouse = inspector.get_columns('Warehouse')
# # columns_inventory = inspector.get_columns('Inventory')
# # columns_productcount = inspector.get_columns('ProductCount')
# # columns_person = inspector.get_columns('Person')

# # print("\nProduct columns:")
# # for column in columns_product:
# #     print(f"Column: {column['name']}, Type: {column['type']}")

# # print("\nWarehouse columns:")
# # for column in columns_warehouse:
# #     print(f"Column: {column['name']}, Type: {column['type']}")

# # print("\nInventory columns:")
# # for column in columns_inventory:
# #     print(f"Column: {column['name']}, Type: {column['type']}")

# # print("\nProductCount columns:")
# # for column in columns_productcount:
# #     print(f"Column: {column['name']}, Type: {column['type']}")

# # print("\nPerson columns:")
# # for column in columns_productcount:
# #     print(f"Column: {column['name']}, Type: {column['type']}")
