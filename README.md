# ITGMKNJ


## Project Scope
* A simple, fast yet efficient and easy-to-use program to scrape any government website with maximum effectiveness and precision to the level according to the user's satisfaction.
* A clean and manageable API to search through the extracted and cleaned data.



## Project Video

https://drive.google.com/file/d/1isJXGWf9jEIPkovuaGDGGsN2Dn0vsTCs/view?usp=sharing


## Installation (Dependencies)

```bash
pip install -r requirements.txt
```

# Execution of Code
## Scraping Data for different Countries
1. Go to folder - 'scrapping_scripts'
```bash
cd Code/scrapping_scripts
```
2. run itgmknj.py
```python3
python itgmknj.py
```
3. Enter the Country Name
4. Enter the Country Link
5. The python script will scrape and store data in 'Code/scrapping_scripts/ScrappedData/PoliticalLeaders.csv' for a given level of deep links.
6. You will asked if you wish to continue. For a yes, the python script will rerun for the next levels of deep links. This will continue until you submit 'no' as the answer. 



## CSV to Database
1. Go to folder - 'Code'
```bash
cd Code
```
2. To setup a sqlite database
```python3
python manage.py migrate
```
3. Run manage.py
```python3
python manage.py runserver
```
4. Go to Localhost:8000/db/personalities - All the data gets copied from csv to database 

## Using Search API
1. Go to folder - 'Code'
```bash
cd Code
```
2. Run manage.py
```python3
python manage.py runserver
```
3. Put the link on Postman to fetch all the data in the database.
```bash
localhost:8000/api/personalities
```
4. A query string will fetch the database entries with relevant entries.
```bash
localhost:8000/api/personalities?first_name=Elizabeth&&middle_name=Bloomer&&last_name=Ford&&full_name=Elizabeth+Bloomer+Ford
```



## Scope of Improvement
* 'genderize' python package used to identify the gender handles only upto 1000 requests per day.
* Since the accuracy of the name identification package 'nameparser' is limited, some redundant data is being stored in the csv file. To increase the accuracy of data, more accurate apis like monkey-learn (paid) can be used.
* The accuracy of the two models (one that identifies useful links for web crawling and other that identifies useful class names and tags) ca be increased by training it over a larger dataset.



## License
[MIT](https://choosealicense.com/licenses/mit/)
