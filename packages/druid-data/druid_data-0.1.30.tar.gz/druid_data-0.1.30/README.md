# DruidData 
![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.7%20|%203.8|%203.9&color=blue?style=flat-square&logo=python) ![PyPI version](https://badge.fury.io/py/druid_data.svg) ![PyPi monthly downloads](https://img.shields.io/pypi/dm/druid_data)

A library to store and retrieve python objects in a DynamoDB database. It supports the basic CRUD operations

## Features
* **[ConstantString]()** - An enum that holds constant values for parameter names

* **[DynamoDBGlobalConfiguration:]()** - A singleton to define global parameters related to DynamoDB

* **[dynamo_entity]()** - A decorator for classes whose objects will be stored in and retrieved from the database

* **[DynamoCrudRepository]()** - A general tool to execute CRUD operations on DynamoDB using the classes decorated with the dynamo_entity decorator, we recommend using the extensions of this class: **SingleTableDynamoCrudRepository** and **MultiTableDynamoCrudRepository** instead of this generic class

* **[SingleTableDynamoCrudRepository]()** - An extension of the DynamoCrudRepository specifically for SingleTable design

* **[MultiTableDynamoCrudRepository]()** - An extension of the DynamoCrudRepository specifically for Mutitable design

### Installation
With [pip](https://pip.pypa.io/en/latest/index.html) installed, run: ``pip install druid_data``

## License

This library is licensed under the MIT-0 License. See the LICENSE file.