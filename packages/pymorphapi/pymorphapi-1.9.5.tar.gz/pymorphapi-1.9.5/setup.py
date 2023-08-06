"""
Module created by Joe Titra: v1.9.5
Used for the Morpheus HOL Test Drive events
v1.5 - added email functions
v1.6 - added option for return data type for invoke_api
v1.7 - added filter_dict and update_price_set functions
v1.8 - corrected issue in update_price_set function
v1.9 - added get_resource_pool_id function
v1.9.1 - added content_type input and debug to invoke_api function
v1.9.2 - added get_item_to_schedule function
v1.9.3 - added create_option_list_data_set and convert_xlsx_sheet_into_json function
v1.9.4 - added validate_naming, import_token_from_cypher, and commit_token_to_cypher
v1.9.5 - added execute_task_on_instance
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymorphapi",
    version="1.9.5",
    description="Common Morpheus API calls for HOL Events",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joe Titra",
    author_email="jtitra@gmail.com",
    url="https://github.com/joetitra/pymorphapi",
    license="MIT License",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "requests"
    ]
)
