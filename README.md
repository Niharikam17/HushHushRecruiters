# Hush Hush Recruiters

---

<h3><u>1. Project Structure:</u></h3>

```
bdp_oct_2022-group_04
│   README.md
│   requirements.txt    
│
│
└───chromedriver
│   │   chromedriver.exe
│   
│
└───data_manipulation
│   │   data_cleaning.py
│   │   data_imputation.py
│   │   model_creation.py
│   │
│   └───Trained_Models
│       │   answers-model.pkl
│       │   questions-model.pkl
│  
└───database
│   │   connector.py
│   │   util.py
│   │   
│   │
└───hh_email
│   │   email_sender.py
│   │   
│   │
└───hushhush
│   │   app.py
│   │   
│   │
└───scoring_system
│   │   score_regressor.py
│   │   scoring_model.py
│   │
│   └───Regression_Model
│       │   regression-model.pkl
│      
│   
└───scraping
│   │   collect_urls.py
│   │   create_search_queries.py
│   │   extract_profile_data.py
│   │
│   └───Text_Files
│       │   cities.txt
│       │   job_profiles.txt
│ 
└───stackexchange_api
│   │   extract_data_from_api.py
│   │   
│   │
└───views
│   │   coding.html
│   │   manage.html
│   │   thank_you.html
│   │
│   └───css
│   │   │   style.css
│   │   
│   │
│   └───js
│       │   coding.js
│       │   manage.js
```

<h3><u>2. Setup Procedure:</u></h3>

1. Navigate to the directory where you want to set up this project.
<br><br>
2. Open cmd/bash and run the below command:<br>
On Mac/Win: ``git clone https://github.com/Big-Data-Programming/bdp_oct_2022-group_04.git`` 
<br><br>
3. Switch to your respective branch:<br>
On Mac/Win: ``git checkout [branch_name]``
<br><br>
4. Now create a virtual enviroment. <br>
On Mac: ``python3 -m venv ./venv``<br>
Example: ``python3 -m venv ./venv``
<br><br>
On Win: ``python -m venv  "[Path to bdp_oct_2022-group_04 Directory]\[NAME_OF_VIRTUAL_ENV]"``<br>
Example: ``python -m venv "D:\bdp_oct_2022-group_04\venv"``
<br><br>
5. To activate the venv run the below command. <br>
On Mac: ``source venv/bin/activate`` <br>
On Win: ``venv\Scripts\activate.bat``
<br><br>
6. To install all the requirements run the below command. Execute this command whenever there is a change in requirements.txt file.<br>
On Mac/Win: ``pip install -r requirements.txt``

<h3><u>3. Application Flow:</u></h3>

1. Inside the hushhush package we have app.py. Run this app.py.
2. Then open manage.html in your browser which is inside view folder.
3. This HTML contains a configuration using which we can select which all procedure we want to execute and how many candidated we are interested in selecting for the coding challenge.
4. Selected candidates will recieve an email, which contains the link to a coding challenge which has an expiry window of 24 Hours. After submitting the coding challenge it will redirect the user to a thank-you page.
5. Candidates who pass this challende will get an interview invitation and those who fail will just get a thank-you email.
