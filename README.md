# About sslv_web_scraper application:
Purpouse: This application will parse https:/ss.lv website for apartments for sale in specific city of your choice
(currently its hardcoded for Ogre city please adjust to your needs) and  will send report filtered by your criteria to your gmail address 

TODO: Add list of features that are implemented

# How to use application:
1. Install requirements python3.7+ , requests, bs4
2. Update gmailer.py file with your email address and password
3. Run app: python3 app.py
4. Report should arrive to email

# TODO Backlog
- [x] Parse website and save data as raw-data report file 
- [x] Add feature print report in one line: URL : message deatails : price
- [ ] Add master page subpage detection and iteration feature
- [x] Code for send gmail implemented and tested and working
- [x] Add send email results via gmail option (can be automated as cron job)
- [x] Send email string that was read from text file 
- [ ] Add feature message filter option by other criteria: example messages only with 2 rooms etc
- [ ] Add Data sience methods and prittify reports
- [ ] Print min/max/average prices as charts 



  
