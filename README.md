# Group 100 Project Overview

## MedWise - Personalized Drug and Nutrition Interaction Alert System
## Summary:
MedWise is a web application designed to help patients manage their medication safety by analyzing potential drug-drug and drug-food interactions based on their past prescription history. By integrating Electronic Health Record (EHR) data with standardized drug interaction databases such as RxNorm, Diet-Drug Interaction Database (DDID), nSIDES Database, and DrugBank, the system will alert users to potential harmful interactions and provide guidance on safe medication and dietary choices.

**Disclaimer: This web service is provided for educational and informational purposes only and does not constitute providing medical advice or professional services.**

## Starting the app:

Before beginning, make sure the MySQL 8.0 database is running on port 3306, then in a python3 eniviorment, run:
```
python .\server\manage.py runserver 
```
To start the django backend. Then run:
```
npm run --prefix .\frontend dev
```
for a development server. If there is an error about next not being installed (if for example, starting the project for the first time) first run ```npm --prefix .\frontend install next``` in order to cache all the node.js modules. 

For a production level server use:
```
npm run --prefix .\frontend start
```