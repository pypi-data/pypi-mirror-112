# [Qualys API Best Practices Series](https://blog.qualys.com/tag/api-best-practices-series) 

BETA Release of Example code from the [Qualys API Best Practices Series](https://blog.qualys.com/tag/api-best-practices-series) 
enhanced with some packaging and operational capability. 
- Important Information
   - An accompanying video will be available from Qualys by July 9th, 2021, Part 3 - Host List Detection.   
      - Hold off on using this software until Part 3 - Host List Detection is released as part of the [Qualys API Best Practices Series](https://blog.qualys.com/tag/api-best-practices-series)
   - See [Roadmap](#roadmap) for additional details.  
   - See [Python Package Index for Qualys ETL](https://pypi.org/project/qualysetl/) for latest version of qualysetl.
   
   - See [Quick Start](#quick-start) to get started now.

## Example: ETL Host List Detection Data
>> ```qetl_manage_user -u [path] -e etl_host_list_detection```
>>
>     - qetl_manage_user will create csv, json and sqlite from Host List Detection Endpoint
>     - sqlite database will contain three tables:  
>       1) Q_Host_List_Detection - Host List Detection Data from vm_processed_after - utc.now to now
>          - Host List Detection Endpoint: 
>            /api/2.0/fo/asset/host/vm/detection/?action=list
>       2) Q_Host_List - Host List Data from vm_processed_after to now
>          - Host List Endpoint:
>            /api/2.0/fo/asset/host/?action=list
>       3) Q_KnowledgeBase_In_Host_List_Detection - corresponding QIDs from Q_Host_List_Detection
>          - KnowledgeBase Endpoint:  
>            /api/2.0/fo/knowledge_base/vuln/?action=list
>
### Output of qetl_manage_user - See SQLite3 Database Tables 

[![](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)


## Table of contents
* [Quick Start](#quick-start)
   * [Install](#installation)
   * [Uninstall](#uninstall)
* [Qualys API Best Practices Series](#qualys-api-best-practices-series)
   * [Workflow Diagram](#workflow-diagram)
   * [Component Diagram](#component-diagram)
   * [Blueprint](#blueprint)
   * [Technologies](#technologies) 
* [ETL Examples](#etl-examples)
    * [ETL KnowledgeBase](#etl-knowledgebase)
    * [ETL Host List](#etl-host-list)
    * [ETL Host List Detection](#etl-host-list-detection)
* [Application Manager and Data](#application-manager-and-data)
    * [Host List Detection SQLite Database](#host-list-detection-sqlite-database)
    * [Data Formats](#data-formats)
    * [Logging](#logging)
    * [Application Monitoring](#application-monitoring)
* [Securing Your Application in the Data Center](#securing-your-application-in-the-data-center)
    * [Password Vault](#password-vault)
* [Example Run Logs](#example-run-logs)
    * [Uninstall and Install qetl](#uninstall-and-install-qetl)
    * [qetl_setup_python_env](#qetl_setup_python_env)  
    * [qetl_manage_user](#qetl_manage_user)
    * [qetl_manage_user Add User](#qetl_manage_user-add-user)
    * [qetl_manage_user ETL KnowledgeBase](#qetl_manage_user-etl-knowledgebase)
    * [Review ETL KnowledgeBase Data](#review-etl-knowledgebase-data)
* [Roadmap](#roadmap)
* [License](#license)
* [ChangeLog](#changelog)


## Quick Start

> Hold off on running until in beta >0.8.0 release.  Contact David Gregory for details.

### Prerequisites Python Module
     1) Ubuntu 20.04
     2) Python 3.8.5 or Latest Stable Release
     3) On base 20.04 you'll need two additional packages.
        sudo apt-get install python3-venv  
        sudo apt install python3-pip
     4) Disk Space on Host.  
        - 100,000 hosts, expect ~400 Gigabytes for full copy of VM Data (Confirmed, Potential, Info Gathered)
        - KnowledgeBase - expect ~1 Gigabyte.
        - Host List - expect ~10 Gigabyte for 100K Hosts.
        - Host List Detection - expect ~300-400 Gigabytes for 100K Hosts.

### Installation

#### First Time Setup Activity
 - Login as "non-root" user that will run qualysetl.
 - sudo root authorization required.
 - Create your /opt/qetl application directory
 - update apt package cache
 - Install python3-venv
 - Install python3-pip
 - Install sqlite3 
 - Install sqlite3 sql browser 

#### First Time Setup Instructions
```bash
#!/usr/bin/env bash
# First Time Setup - Pre-create directory /opt/qetl
# Login as user that will execute qetl_manage_user
sudo mkdir /opt/qetl    
sudo chown $USERNAME /opt/qetl
sudo chgrp $USERNAME /opt/qetl
sudo apt update
sudo apt install -y python3-venv python3-pip sqlite3 sqlitebrowser
```

#### Install or Upgrade QualysETL activity
 - Login as "non-root" user that will run qualysetl.
 - deactivate to exit any current python virtual environment you may be in.
 - Install/Upgrade qualysetl into your /home/$USERNAME/.local python directory
 - Create qualysetl python virtual environment in /opt/qetl/qetl_venv, 
   installing all required modules in venv
 - Execute qualysetl to see help screen


#### Install or Upgrade QualysETL Instructions

```bash
#!/usr/bin/env bash
# Login as user that will execute qetl_manage_user
# Install Application in Python Virtual Environment /opt/qetl/qetl_venv
deactivate  2>/dev/null   # Ensure you are not in a python virtual environment, error is ok.
python3 -m pip install --upgrade qualysetl
/home/$USERNAME/.local/bin/qetl_setup_python_venv /opt/qetl
echo "Follow instructions output from qetl_setup_python_venv"
```

### Create your first qualysetl user
To setup your first user, you'll need your qualys api username, password and your api fqdn.

Example transcript of setting up a new user

```bash
qualysetl@ubuntu:~$ source /opt/qetl/qetl_venv/bin/activate
(qetl_venv) qualysetl@ubuntu:~$ qetl_manage_user -u /opt/qetl/users/quays_dt4

qetl_user_home_dir does not exist: /opt/qetl/users/quays_dt4/qetl_home
Create new qetl_user_home_dir? /opt/qetl/users/quays_dt4/qetl_home ( yes or no ): yes

qetl_user_home_dir created: /opt/qetl/users/quays_dt4/qetl_home

Current username: initialuser in config: /opt/qetl/users/quays_dt4/qetl_home/cred/.etld_cred.yaml
Update Qualys username? ( yes or no ): yes
Enter new Qualys username: quays_dt4
Current api_fqdn_server: qualysapi.qualys.com
Update api_fqdn_server? ( yes or no ): 
Enter new api_fqdn_server: qualysapi.qualys.com
Update password for username: quays_dt4
Update password? ( yes or no ): yes
Enter your Qualys password: 
You have updated your credentials.
  Qualys Username: quays_dt4
  Qualys api_fqdn_server: qualysapi.qualys.com


Would you like to test login/logout of Qualys? ( yes or no ): yes

Qualys Login Test for quays_dt4 at api_fqdn_server: qualysapi.qualys.com

Testing Qualys Login for quays_dt4 Succeeded at qualysapi.qualys.com
    with HTTPS Return Code: 200.

Thank you, exiting.

(qetl_venv) qualysetl@ubuntu:~$ 

```

### Execute your first ETL.
Your initial configuration limits the total hosts downloaded to 1000 hosts vm_processed_after 
utc.now - 1 day.  The initial configuration will only consume up to 2 connections.
You can test this to ensure you are able to download data before moving on to more data.
- Command - qetl_manage_user -u /opt/qetl/users/quays_dt4 -e etl_host_list_detection
- Ouputs: 
     - Full Knowledgebase on first run.
     - Host List vm_processed_after utc.now - 1 day limited to 1000 hosts for testing. 
     - Host List Detection driven by scope of Host List.

Transcript of command execution.  
```bash
qetl_manage_user -u /opt/qetl/users/quays_dt4 -e etl_host_list_detection
Starting etl_host_list_detection.  For progress see: /opt/qetl/users/quays_dt4/qetl_home/log/host_list_detection.log
Ending   etl_host_list_detection.  For results see: /opt/qetl/users/quays_dt4/qetl_home/log/host_list_detection.log
sqlitebrowser /opt/qetl/users/quays_dt4/qetl_home/data/host_list_detection_sqlite.db 
```
SQLite Browser displaying Knowledgebase, Host List and Host List Detection. Note that the knowledgebase in this database 
only includes qids found in host list detection.  To see the full knowledgebase, open kb_sqlite.db.

[![](https://user-images.githubusercontent.com/82658653/122690720-20115200-d1f9-11eb-9382-7e80a7222e47.png)](https://user-images.githubusercontent.com/82658653/122690720-20115200-d1f9-11eb-9382-7e80a7222e47.png)


### Uninstall

Uninstall qualysetl activity.
  - deactivate to exit any current python virtual environment you may be in.
  - optionally remove application/data:
    - python virtual environment: /opt/qetl/qetl_venv
    - qualysetl data directory: /opt/qetl/users
    - python3-venv 
    - python3-pip
    - sqlite3
    - sqlitebroswer
    
```bash
#!/usr/bin/env bash
deactivate  # If you are in a python virtual environment
python3 -m pip uninstall qualysetl
# Optionally remove python virtual env, pip, sqlite3, sqlitebrowser and users application data.
# cd /opt/qetl/
# rm -ir qetl_venv  # Optionally remove qetl_venv
# rm -ir users      # Optionally remove users directory with data
# sudo apt remove -y python3-venv python3-pip sqlite3 sqlitebrowser
```

- Jump to [ETL Examples](#etl-examples) to transform Qualys data into CSV, JSON and SQLite Databases.

## Qualys API Best Practices Series
The example code from the [Qualys API Best Practices Series](https://blog.qualys.com/tag/api-best-practices-series) 
is being hosted here to help customers with an example blueprint to automate transformation 
of data into their corporate data systems, further enhancing the visibility of outlier systems 
that are vulnerable.  

This example code has been enhanced with some exception processing, logging, and a single point of execution
creating an operational context within which to test/develop the code so customers can build automation 
into their remediation program. 

### Workflow Diagram
The workflow depicts the flow of etl for host list detection.  The key output is the sqlite database that is ready for distribution
- qetl_manage_user -u [userdir] -e etl_host_list_detection -d [datetime] - Resulting sqlite database ready for distribution.

[![](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)

### Component Diagram
The component diagram depicts major system interoperability components that deliver data into the enterprise.

Component | Color | Purpose
------------ | ------------- | -------------
Execution Environment | Blue | Host and Cloud where this application operates
Application | Grey | Application context to identify Local Docker, Python Application, Host and/or Filesystems
Input | Orange | Qualys data consumed by application
Execution | Green | Execution ETL of Qualys Data through various methods.  (The Python Execution Environment on Docker or Traditional Host)
Data | Yellow | Host Data Folders that separate Application, and Subscription Data Users along with distribution pipelines representing the distribution of data to external sources, Cloud, Client, Other
Future | Black | TBD Future State Components such as GraphQL Server.

[![](https://user-images.githubusercontent.com/82658653/120926641-c1ea5800-c6ab-11eb-832b-1af03f77462a.png)](https://user-images.githubusercontent.com/82658653/120926641-c1ea5800-c6ab-11eb-832b-1af03f77462a.png)

### Blueprint
Customer have many options for Qualys API integration today.  Some customers realize they need to develop their own 
internal code to transform complex data, create custom metrics, create custom reports or ensure data is more accessible within their organizations for metrics and custom reporting.

As a result, Qualys decided on creating the API Best Practices Series to jumpstart clients with a blueprint of example code
to help them automate delivery of complex data into their enterprise.  

The overarching goal is to simplify our customers security stack and help them significantly reduce cost and 
complexity.

Key Goals and Solutions of this series are:

Goal | Solution
------------ | -------------
Automate Vulnerability Data accessibility, transformation of complex data for analysis | JSON, CSV, SQLite Database Formats of Qualys Data readily accessible to Analytical BI Tools for on-demand analysis or for downstream loading into Enterprise Data Storage.
A single query interface to Qualys data | TBD Future GraphQL Server interface to data.
Automate Capturing Vulnerability Data into corporate processes | Blueprint of example code customers can customize to enhance their internal automation "API-First" strategy.
Automate Distribution of Vulnerability Data to Cloud Providers | Optional Distribution methods into cloud systems such as Amazon S3 Bucket
Automate Application Enhancements and Delivery | Docker application instance for reliable CI/CD delivery of enhancements, as well as traditional host execution on Linux Platforms.
Provide Execution Flexibility, Work Load Management, Password Security | Blueprint for enterprise jobstream execution (Ex. Autosys), password vaults (Ex. Hashicorp), or simple command line execution from a Virtual Machine instance of Ubuntu running on a laptop.
Provide Continous Vulnerability Data Pipeline | Blueprint for data transformation pipeline from Qualys to Enterprise Data Stores in various formats ( JSON, CSV, SQLite Database ) 


## Technologies
Project tested with:
1. Ubuntu version: 20.04
2. SQLite3 version: 3.31.1
3. GNU DBM version: 1.18 
4. Python version: 3.8.5 
6. Qualys API: latest

## ETL Examples
- Create XML, JSON, CSV and SQLite3 Database Formats of Qualys Data.

### ETL Configuration 
- Configuration file: /opt/qetl/users/[quser]/qetl_home/config/etld_config_settings.yaml
- Ensure you set these configurations:
  1. host_list_detection_concurrency_limit: 2   
     Set this to appropriate qualys concurrency limit value after 
     reviewing the [Qualys Limits Guide](https://www.qualys.com/docs/qualys-api-limits.pdf) 
     https://www.qualys.com/docs/qualys-api-limits.pdf with your TAM for Questions. 
  2. host_list_detection_limit_hosts: 1000      
     Set this to 1000000.  It is defaulted to 1000 for first run testing.
     If you have over 1000000 ( 1 Million ) hosts, please contact your TAM 
     and request meeting with David Gregory 
  3. [kb, host_list, host_list_detection]_csv_truncate_cell_limit variables          
     Truncates cells to integer value in both csv and sqlite database.  Set to what you are comfortable with.  It defaults to 32K to ensure you can read the csv in excel, and it also truncates the cell size sent to the sqlite database.

```bash
(qetl_venv) qualysetl@ubuntu:~/.local/bin$ more /opt/qetl/users/qualysetl/qetl_home/config/etld_config_settings.yaml 
#
# This file is generated by qetl_manage_user only on first invocation.
# File generated by qetl_manage_user on: 2021-06-17 20:40:59
#
# YAML File of available configuration options for Qualys API Calls and future options.
# Ensure you set these configurations:
#
#     1) host_list_detection_concurrency_limit: 2
#         - Set this to appropriate qualys concurrency limit value after reviewing the
#           [Qualys Limits Guide] https://www.qualys.com/docs/qualys-api-limits.pdf with your TAM for Questions.
#           Note: if you exceed the endpoints concurrency limit,
#                 the application will reset the concurrency limit to X-ConcurrencyLimit-Limit - 1
#
#     2) host_list_detection_limit_hosts: 1000
#         - defaulted to 1000 for first run testing. This is an integer with no commas.
#         - Set this to a number you are comfortable with.
#         -     Example 1: If you have 100,000 hosts max in your subscription, set the value to 100000
#         -     Example 2: If you have 1,000,000 hosts max in your subscription, set the value to 1000000
#         - If you have over 1000000 ( 1 Million ) hosts, please contact your TAM and schedule
#           a meeting with David Gregory. 
#
#     3) truncate_cell_limit
#        i.   kb_csv_truncate_cell_limit                    - KnowledgeBase cell truncation
#        ii.  host_list_csv_truncate_cell_limit             - Host List cell truncation
#        iii. host_list_detection_csv_truncate_cell_limit   - Host List Detection cell truncation
#         Truncates cells to integer value in both csv and sqlite database.
#           Set to what you are comfortable with. It defaults to 32K to ensure
#           you can read the csv in excel,
#         Note:  This value truncates the cell size sent to the sqlite database.
#
#
# kb_last_modified_after: 'default'                  # Leave at default.  Knowledgebase is auto-incremental 
#                                                      to full knowledgebase.
# kb_export_dir: 'default'                           # Leave at default.  If local directory path is added, 
#                                                      the program will copy csv, json, sqlite files there.
# kb_payload_option: 'default'                       # Leave at default until future use is developed.
# kb_csv_truncate_cell_limit: 32000                  # Truncate all cells to integer.  Useful for reading 
#                                                      csv in excel. Will also truncate database cells.
#
# host_list_vm_processed_after: 'default'            # Leave at default.  handle dates through qetl_manage_user
# host_list_payload_option: 'notags'                 # Leave at 'notags' until future use is developed.
# host_list_export_dir: 'default'                    # Leave at default.  If local directory path is added, 
#                                                      the program will copy the csv, json, sqlite files there.
# host_list_csv_truncate_cell_limit: 32000           # Truncate all cells to integer.  Useful for reading csv 
#                                                      in excel. Will also truncate database cells.
#
# host_list_detection_payload_option: 'default'      # Leave at 'default' until future use is developed.
# host_list_detection_export_dir: 'default'          # Leave at default.  If local directory path is added, the 
#                                                      program will copy the csv, json, sqlite files there.
# host_list_detection_vm_processed_after: 'default'  # Leave at default.  dates are handled through qetl_manage_user
# host_list_detection_concurrency_limit: 2           # Reset based on limits guide:  
#                                                      https://www.qualys.com/docs/qualys-api-limits.pdf
# host_list_detection_multi_proc_batch_size: 750     # Leave at 750
# host_list_detection_limit_hosts: 1000              # Set to the maximum number of hosts in your subscription.
#                                                    # If unsure, set to 1000000 ( 1 million ).  If you have over 
#                                                    # 1000000 hosts, please contact dgregory@qualys.com
# host_list_detection_csv_truncate_cell_limit: 32000 # Truncate all cells to integer.  Useful for reading csv 
#                                                      in excel. Will also truncate database cells.

kb_last_modified_after: 'default'
kb_export_dir: 'default'
kb_payload_option: 'default'
kb_csv_truncate_cell_limit: 32000

host_list_vm_processed_after: 'default'
host_list_payload_option: 'notags'
host_list_export_dir: 'default'
host_list_csv_truncate_cell_limit: 32000

host_list_detection_payload_option: 'default'
host_list_detection_export_dir: 'default'
host_list_detection_vm_processed_after: 'default'
host_list_detection_concurrency_limit: 2
host_list_detection_multi_proc_batch_size: 750
host_list_detection_limit_hosts: 1000
host_list_detection_csv_truncate_cell_limit: 32000
```

### ETL KnowledgeBase
KnowledgeBase ETL - Incremental Update to Knowledgebase.  CSV, JSON, SQLite are full knowledgebase.  XML is incremental.
   - note the knowledgebase will rebuild itself every 30-90 days to ensure gdbm is reorganized.
```bash
qetl_manage_user -u /opt/qetl/users/quser -e etl_knowledgebase 
```

### ETL Host List
Host List ETL - Download Host List based on date
  - if no date is used, Host List will auto increment from last run 
    ( max LAST_VULN_SCAN_DATETIME ) or if no sqlite database exists
    it download start incremental pull from utc minus 1 day. 
```bash
qetl_manage_user -u /opt/qetl/users/quser -e etl_host_list -d [YYYY-MM-DDThh:mm:ssZ]
```
   
See [Application Manager and Data](#application-manager-and-data) for location of your qetl_home directory.
   
### ETL Host List Detection
Host List Detection ETL - Includes KnowledgeBase and Host List so do not run ETL Host List or ETL KnowledgeBase while Host List Detection ETL is runnning..
  - if no date is used, The Host List Driver will auto increment from last run
      ( max LAST_VULN_SCAN_DATETIME ) or if no sqlite database exists
      it download start incremental pull from utc minus 1 day. 
```bash
qetl_manage_user -u /opt/qetl/users/quser -e etl_host_list_detection -d [YYYY-MM-DDThh:mm:ssZ]
```

## Application Manager and Data

### qetl_manage_user application
- qetl_manage_user is your entry point to manage ETL of Qualys Data.

[![](https://user-images.githubusercontent.com/82658653/122486122-6a4ec500-cfa6-11eb-8605-6115f9b0950d.png)](https://user-images.githubusercontent.com/82658653/122486122-6a4ec500-cfa6-11eb-8605-6115f9b0950d.png)

### Host List Detection SQLite Database
- qetl_manage_user -u [userdir] -e etl_host_list_detection -d [datetime] - Resulting sqlite database ready for distribution.


[![](https://user-images.githubusercontent.com/82658653/120927089-a1bb9880-c6ad-11eb-8b83-98c3e7643473.png)](https://user-images.githubusercontent.com/82658653/120927089-a1bb9880-c6ad-11eb-8b83-98c3e7643473.png)


### Host List Detection SQLite Tables
- qetl_manage_user -u [userdir] -e etl_host_list_detection -d [datetime] - Resulting sqlite database ready for distribution.

[![](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)

### Environment
   - Python virtual environment 
   - Managed by qetl_manage_user
   - Example options for qetl Home Directories:
       - Prod: /opt/qetl/users/[user_name]/qetl_home
       - Test: /usr/local/test/opt/qetl/users/[user_name]/qetl_home
       - Dev:  $HOME/opt/qetl/users/[user_name]/qetl_home
    
### Application Directories

Path | Description
------------ | -------------
   opt/qetl/users/ | Directory of All Users 
   opt/qetl/users/[user]/qetl_home | Parent directory path for a user
   [user]/qetl_home | User Home Directory
   qetl_home/bin | User bin directory for customer to host scripts they create.
   qetl_home/cred | Credentials Directory
   qetl_home/cred/.etld_lib_credentials.yaml | Credentials file in yaml format.  
   qetl_home/cred/.qualys_cookie | Cookie file used for Qualys session management.
   qetl_home/config | Application Options Configuration Directory
   qetl_home/config/etld_lib_config_settings.yaml | Application Options
   qetl_home/log | Logs Directory
   qetl_home/log/kb.log | KnowledgeBase Run Logs
   qetl_home/log/host_list.log | Host List Run Logs
   qetl_home/log/host_list_detection.log | Host List Detection Run Logs
   qetl_home/data | Application Data Directory containing all csv, xml, json, sqlite database data.
   qetl_home/data/kb.csv | Cumulative Knowledgebase CSV file.
   qetl_home/data/kb_shelve | Cumulative Knowledgebase Python Shelve
   qetl_home/data/kb.xml | Incremental update Knowledgebase XML File
   qetl_home/data/kb.json | Cumulative Knowledgebase JSON Data
   qetl_home/data/kb_sqlite.db | Cumulative Knowledgebase SQLite Database
   qetl_home/data/kb_cve_qid_map.csv | Cumulative CVE -> QID List CSV File
   qetl_home/data/kb_cve_qid_map_shelve | Cumulative CVE -> QID List Python Shelve 
   qetl_home/data/host_list.json | vm_last_processed Host List JSON Data
   qetl_home/data/host_list_shelve | vm_last_processed Host List Python Shelve
   qetl_home/data/host_list_sqlite.db | vm_last_processed Host List SQLite Database
   qetl_home/data/host_list.csv | vm_last_processed Host List CSV File
   qetl_home/data/host_list_other_file.xml | vm_last_processed Host List XML Data
   qetl_home/data/host_list_detection.json | vm_last_processed Host List Detection JSON Data
   qetl_home/data/host_list_detection_shelve |	vm_last_processed Host List Detection Python Shelve
   qetl_home/data/host_list_detection_sqlite.db |	vm_last_processed Host List Detection SQLite Database
   qetl_home/data/host_list_detection.csv |	vm_last_processed Host List Detection CSV File
   qetl_home/data/host_list_detection_xml_dir |	vm_last_processed Host List Detection XML Data Dir


### Data Formats 
Data Formats created in qetl_home/data:

Format | Description
------------ | -------------
JSON | [Java Script Object Notation](https://datatracker.ietf.org/doc/html/rfc7159) useful for transfer of data between systems
CSV | [Comma Separated Values](https://datatracker.ietf.org/doc/html/rfc4180) useful for transfer of data between systems<br>Formatted to help import data into various BI or Database Tools:  Excel, Apache Open Office, Libre Office, Tableau, Microsoft PowerBI, SQL Database Loader
XML | [Extensible Markup Language](https://datatracker.ietf.org/doc/html/rfc3470) useful for transfer of data between systems
SQLite Database | [SQLite Database](https://www.sqlite.org/about.html): SQLite Database populated with Qualys Data, Useful as a self-contained SQL Database of Qualys Data for Analysis, Useful as an intermediary transformation into your overall Enterprise ETL Process, SQLite is an in-process library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine


### Logging

Logging fields are pipe delimited with some formatting for raw readability.  You can easily import this data into excel, 
 a database for analysis or link this data to a monitoring system.

Format | Description
------------ | -------------
YYYY-MM-DD hh:mm:ss,ms | UTC Date and Time.  UTC is used to match internal date and time within Qualys data.
Logging Level | INFO, ERROR, WARNING, etc.  Logging levels can be used for troubleshooting or remote monitoring for ERROR/WARNING log entries.
Module Name: YYYYMMDDHHMMSS | Top Level qetl Application Module Name that is executing, along with date to uniquely identify all log entries associated with that job.
User Name | Operating System User executing this application.
Function Name | qetl Application Function Executing.
Message | qetl Application Messages describing actions, providing data.


See [Application Directories](#application-directories) for details of each log file.
```bash
cd qetl_home/log
head -3 kb.log
(qetl_venv) qualysetl@ubuntu:/opt/qetl/qetl_venv/bin$ cat /opt/qetl/users/qualys_user/qetl_home/log/kb.log | nl 
     1	2021-05-28 01:26:03,836 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_logging_stdout                | LOGGING SUCCESSFULLY SETUP FOR STREAMING
     2	2021-05-28 01:26:03,836 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_logging_stdout                | PROGRAM: ['/home/dgregory/opt/qetl/qetl_venv/bin/qetl_manage_user', '-u', '/opt/qetl/users/qualys_user', '-e', 'etl_knowledgebase']
     3	2021-05-28 01:26:03,897 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | check_python_version                | Python version found is: ['3.8.5 (default, Jan 27 2021, 15:41:15) ', '[GCC 9.3.0]']
     4	2021-05-28 01:26:03,897 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | get_sqlite_version                  | SQLite version found is: 3.31.1.
     5	2021-05-28 01:26:03,898 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | set_qetl_code_dir                   | parent qetl code dir - /home/dgregory/opt/qetl/qetl_venv/lib/python3.8/site-packages
```

### Application Monitoring
- To monitor the application for issues, the logging format includes a logging level.  
- Monitoring for ERROR will help identify issues and tend to the overall health of the applicaiton operation.

## Securing Your Application in the Data Center
Follow your corporate procedures for securing your application.  A key recommendation is to use a password vault
or remote invocation method that passes the credentials at run time so the password isn't stored on the system.

### Password Vault
Qualys recommends customers move to a password vault of their chosing to operate this applications credentials.
By creating functions to obtain credentials from your corporations password vault, you can improve 
the security of your application by separating the password from the machine.  

One way customers can do this is through a work load management solution, where the external work load management
system ( Ex. Autosys ) schedules jobs passing the required keys to this application at runtime.  This eliminates
the need to store credentials locally on your system.

If you are unfamiliar with password vaults, here is one example from Hashicorp.
- [Hashicorp Products Vault](https://www.hashicorp.com/products/vault)
- [Hashicorp Getting Started](https://learn.hashicorp.com/tutorials/vault/getting-started-intro?in=vault/getting-started)

## Roadmap

Capability | Target | Description
---------- | ------ | -----------
KnowledgeBase | June 2021 | Automate download and transform of KnowledgeBase into CSV, JSON and SQLite Database
Host List | June 2021 | Automate download and transform of Host List into CSV, JSON and SQLite Database
Host List Detection | June 2021 | Automate download and transform of Host List Detection into CSV, JSON and SQLite Database
Python Virtual Environment Package | June 2021 | Encapsulate qetl Application into Python Virtual Environment at installation.
Docker Image | July 2021 | Encapsulate Python Application into distributable docker image for ease os operation and upgrade.
Other Modules | TBD Q3/Q4 2021 | Global IT Asset Inventory, Policy Compliance, distribution methods S3 Bucket, etc...

## Example Run Logs

### Uninstall and Install qetl

#### Uninstall Run Log

- Make sure you are not in your Python Virtual Environment when running uninstall.  
  Notice the command prompt does not include (qetl_env).  That means you have deactivated the Python3 Virtual Environment

```bash
(qetl_venv) qualysetl@ubuntu:~$ deactivate

qualysetl@ubuntu:~/.local/bin$ python3 -m pip uninstall qualysetl
Found existing installation: qualysetl 0.6.30
Uninstalling qualysetl-0.6.30:
  Would remove:
    /home/dgregory/.local/bin/qetl_setup_python_venv
    /home/dgregory/.local/lib/python3.8/site-packages/qualys_etl/*
    /home/dgregory/.local/lib/python3.8/site-packages/qualysetl-0.6.30.dist-info/*
Proceed (y/n)? y
  Successfully uninstalled qualysetl-0.6.30
qualysetl@ubuntu:~/.local/bin$ 

```

#### Install

- Make sure you are not in your Python Virtual Environment when installing this software.  
  Notice the command prompt does not include (qetl_env).

```bash
(qetl_env) qualysetl@ubuntu:~$ deactivate
qualysetl@ubuntu:~$ python3 -m pip install qualysetl
Collecting qualysetl
  Downloading qualysetl-0.6.30-py3-none-any.whl (79 kB)
     |████████████████████████████████| 79 kB 1.8 MB/s 
Installing collected packages: qualysetl
Successfully installed qualysetl-0.6.30
qualysetl@ubuntu:~$ 
```

### qetl_setup_python_env

```bash
qualysetl@ubuntu:~/.local/bin$ ./qetl_setup_python_venv /opt/qetl
Start qetl_setup_python_venv - Thu 17 Jun 2021 08:39:41 PM PDT
  1) test_os_for_required_commands
  2) test_for_pip_connectivity
  3) prepare_opt_qetl_env_dirs

    usage:        qetl_setup_python_venv [/path/to/dir]

    description:

        Create a python3 virtual environment, and install the qualysetl application into that environment for usage.
        This isolates the qualysetl application dependencies to the python3 virtual environment.

            If you plan to setup your python virtual environment outside of your default home directory,
            please ensure you have authorization to create directories in the target location.

    examples:
            1) qetl_setup_python_venv /opt/qetl
               - will work if you pre-create /opt/qetl as you have to be root to write to /opt
            2) qetl_setup_python_venv /usr/local
               - will result in /usr/local/opt/qetl if you have authorization to write to /usr/local
            3) qetl_setup_python_venv
               - Default will be your /home/qualysetl/opt/qetl directory.


Create qetl Python Environment? /opt/qetl/qetl_venv
Do you want to create your python3 virtual environment for qetl? ( yes or no ) yes

ok, creating python3 virtual /opt/qetl/qetl_venv


  4) create_qetl_python_venv - will run for about 1-2 minutes

     1	    Package         Version  
     2	    --------------- ---------
     3	    boto3           1.17.97  
     4	    botocore        1.20.97  
     5	    certifi         2021.5.30
     6	    chardet         4.0.0    
     7	    idna            2.10     
     8	    jmespath        0.10.0   
     9	    oschmod         0.3.12   
    10	    pip             20.0.2   
    11	    pkg-resources   0.0.0    
    12	    python-dateutil 2.8.1    
    13	    PyYAML          5.4.1    
    14	    qualysetl       0.6.35   
    15	    requests        2.25.1   
    16	    s3transfer      0.4.2    
    17	    setuptools      57.0.0   
    18	    six             1.16.0   
    19	    urllib3         1.26.5   
    20	    wheel           0.36.2   
    21	    xmltodict       0.12.0   


     1	    Name: qualysetl
     2	    Version: 0.6.35
     3	    Summary: Qualys API Best Practices Series - ETL Blueprint Example Code within Python Virtual Environment
     4	    Home-page: https://dg-cafe.github.io/qualysetl/
     5	    Author: David Gregory
     6	    Author-email: dgregory@qualys.com, dave@davidgregory.com
     7	    License: Apache
     8	    Location: /opt/qetl/qetl_venv/lib/python3.8/site-packages
     9	    Requires: 
    10	    Required-by: 

   Success! Your python virtual environment for qetl is: /opt/qetl/qetl_venv

   Your python3 venv separates your base python installation from the qetl python requirements
   and is your entry to executing the qetl_manage_user application.  Your base qetl installation has
   moved to your python virtual environment: /opt/qetl/qetl_venv

   !!! save these commands as they are your entry to run the qetl application
   
       1) source /opt/qetl/qetl_venv/bin/activate
       2) /opt/qetl/qetl_venv/bin/qetl_manage_user ( Your entry point to operating qualysetl ) 

   Next steps:

    Enter your python3 virtual environment and begin testing qualys connectivity.

       1) source /opt/qetl/qetl_venv/bin/activate
       2) /opt/qetl/qetl_venv/bin/qetl_manage_user

End   qetl_setup_python_venv - Thu 17 Jun 2021 08:40:04 PM PDT
qualysetl@ubuntu:~/.local/bin$
```
### qetl_manage_user
You can execute qetl_manage_user to see options available.  To operate the qetl_manage_user
application you'll first enter the python3 virtual environment, then execute qetl_manage_user.

```bash
(qetl_venv) qualysetl@ubuntu:~/.local/bin$ qetl_manage_user 
    
Please enter -u [ your /opt/qetl/users/ user home directory path ]
    Note: /opt/qetl/users/newuser is the root directory for your qetl userhome directory, 
         enter a new path including the opt/qetl/users/newuser 
         in the path you have authorization to write to.
         the prefix to your user directory opt/qetl/users is required.
         Example:
            1) /opt/qetl/users/newuser

        
    usage: qetl_manage_user [-h] -u qetl_USER_HOME_DIR [-e execute etl module] [-c] [-t] [-d] [-r] [-l]
    
    Setup and execute etl module for your qualys qetl users.  
    
    optional arguments:
      -h, --help                show this help message and exit
      -u Home Directory Path, --qetl_user_home_dir Home directory Path
                                   Include prefix opt/qetl/users/[user dir] 
                                   Examples:
                                   1) /home/dgregory/opt/qetl/users/q_username 
                                   2) /opt/qetl/users/q_username
      -e etl module name,     --execute_etl_module module name
                                  Ex.  -e etl_knowledgebase or -e etl_host_list or -e etl_host_list_detection
      -d YYMMDDThh:mm:ssZ,    --datetime        YYYY-MM-DDThh:mm:ssZ UTC. Get All Data On or After Date. 
      -c, --credentials       update qualys api user credentials: qualys uername, password or api_fqdn_server
      -t, --test              test qualys credentials
      -l, --logs              detailed logs sent to stdout
      -r, --report            brief report of the users directory structure.

```

### qetl_manage_user Add User
To add a new user, execute qetl_manage_user -u [opt/users/your_new_user].  See example run log below.

```bash
qualysetl@ubuntu:~$ source /opt/qetl/qetl_venv/bin/activate
(qetl_venv) qualysetl@ubuntu:~$ qetl_manage_user

        
    
Please enter -u [ your /opt/qetl/users/ user home directory path ]
    Note: /opt/qetl/users/newuser is the root directory for your qetl userhome directory, 
         enter a new path including the opt/qetl/users/newuser 
         in the path you have authorization to write to.
         the prefix to your user directory opt/qetl/users is required.
         Example:
            1) /opt/qetl/users/newuser


        
    usage: qetl_manage_user [-h] -u qetl_USER_HOME_DIR [-e execute etl module] [-c] [-t] [-d] [-r] [-l]
    
    Setup and execute etl module for your qualys qetl users.
    
    optional arguments:
      -h, --help                show this help message and exit
      -u Home Directory Path, --qetl_user_home_dir Home directory Path
                                   Include prefix opt/qetl/users/[user dir]
                                   Examples:
                                   1) /home/dgregory/opt/qetl/users/q_username
                                   2) /opt/qetl/users/q_username
      -e etl module name,     --execute_etl_module module name
                                  Ex.  -e etl_knowledgebase or -e etl_host_list or -e etl_host_list_detection
      -d YYMMDDThh:mm:ssZ,    --datetime        YYYY-MM-DDThh:mm:ssZ UTC. Get All Data On or After Date.
      -c, --credentials       update qualys api user credentials: qualys uername, password or api_fqdn_server
      -t, --test              test qualys credentials
      -l, --logs              detailed logs sent to stdout
      -r, --report            brief report of the users directory structure.
     
    
(qetl_venv) qualysetl@ubuntu:~$ qetl_manage_user -u /opt/qetl/users/qqusr_dt4

qetl_user_home_dir does not exist: /opt/qetl/users/qqusr_dt4/qetl_home
Create new qetl_user_home_dir? /opt/qetl/users/qqusr_dt4/qetl_home ( yes or no ): yes

qetl_user_home_dir created: /opt/qetl/users/qqusr_dt4/qetl_home


Current username: initialuser in config: /opt/qetl/users/qqusr_dt4/qetl_home/cred/.etld_cred.yaml
Update Qualys username? ( yes or no ): yes
Enter new Qualys username: qqusr_dt4
Current api_fqdn_server: qualysapi.qualys.com
Update api_fqdn_server? ( yes or no ): no
Update password for username: qqusr_dt4
Update password? ( yes or no ): yes
Enter your Qualys password:
You have updated your credentials.
  Qualys Username: qqusr_dt4
  Qualys api_fqdn_server: qualysapi.qualys.com


Would you like to test login/logout of Qualys? ( yes or no ): yes

Qualys Login Test for qqusr_dt4 at api_fqdn_server: qualysapi.qualys.com

Testing Qualys Login for qqusr_dt4 Succeeded at qualysapi.qualys.com
    with HTTPS Return Code: 200.

Thank you, exiting.

(qetl_venv) qualysetl@ubuntu:~/opt/qetl/qetl_venv/bin$ 
```

### qetl_manage_user ETL KnowledgeBase

```bash
(qetl_venv) qualysetl@ubuntu:~/opt/qetl/qetl_venv/bin$ qetl_manage_user -u /opt/qetl/users/qualys_user -e etl_knowledgebase
Starting etl_knowledgebase.  For progress see your /opt/qetl/users/qualys_user/qetl_home log directory
End      etl_knowledgebase.  For progress see your /opt/qetl/users/qualys_user/qetl_home log directory

(qetl_venv) qualysetl@ubuntu:~/opt/qetl/qetl_venv/bin$ cat /opt/qetl/users/qualys_user/qetl_home/log/kb.log | nl 
     1	2021-05-28 01:26:03,836 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_logging_stdout                | LOGGING SUCCESSFULLY SETUP FOR STREAMING
     2	2021-05-28 01:26:03,836 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_logging_stdout                | PROGRAM: ['/home/dgregory/opt/qetl/qetl_venv/bin/qetl_manage_user', '-u', '/opt/qetl/users/qualys_user', '-e', 'etl_knowledgebase: 20210528012603']
     3	2021-05-28 01:26:03,897 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | check_python_version                | Python version found is: ['3.8.5 (default, Jan 27 2021, 15:41:15) ', '[GCC 9.3.0]']
     4	2021-05-28 01:26:03,897 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | get_sqlite_version                  | SQLite version found is: 3.31.1.
     5	2021-05-28 01:26:03,898 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | set_qetl_code_dir                   | parent qetl code dir - /home/dgregory/opt/qetl/qetl_venv/lib/python3.8/site-packages
     6	2021-05-28 01:26:03,898 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | set_qetl_code_dir                   | child qetl code dir  - /home/dgregory/opt/qetl/qetl_venv/lib/python3.8/site-packages/qualys_etl
     7	2021-05-28 01:26:03,898 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | set_qetl_code_dir                   | etld_lib              - /home/dgregory/opt/qetl/qetl_venv/lib/python3.8/site-packages/qualys_etl/etld_lib
     8	2021-05-28 01:26:03,898 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | set_qetl_code_dir                   | etld_templates        - /home/dgregory/opt/qetl/qetl_venv/lib/python3.8/site-packages/qualys_etl/etld_templates
     9	2021-05-28 01:26:03,898 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | set_qetl_code_dir                   | etld_knowledgebase    - /home/dgregory/opt/qetl/qetl_venv/lib/python3.8/site-packages/qualys_etl/etld_knowledgebase
    10	2021-05-28 01:26:03,898 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | set_qetl_code_dir                   | etld_host_list        - /home/dgregory/opt/qetl/qetl_venv/lib/python3.8/site-packages/qualys_etl/etld_host_list
    11	2021-05-28 01:26:03,900 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_user_home_directories         | parent user app dir  - /opt/qetl/users/qualys_user
    12	2021-05-28 01:26:03,900 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_user_home_directories         | user home directory  - /opt/qetl/users/qualys_user/qetl_home
    13	2021-05-28 01:26:03,900 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_user_home_directories         | qetl_user_root_dir   - User root dir       - /opt/qetl/users
    14	2021-05-28 01:26:03,900 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_user_home_directories         | qetl_user_home_dir   - qualys user         - /opt/qetl/users/qualys_user/qetl_home
    15	2021-05-28 01:26:03,900 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_user_home_directories         | qetl_user_data_dir   - xml,json,csv,sqlite - /opt/qetl/users/qualys_user/qetl_home/data
    16	2021-05-28 01:26:03,900 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_user_home_directories         | qetl_user_log_dir    - log files           - /opt/qetl/users/qualys_user/qetl_home/log
    17	2021-05-28 01:26:03,900 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_user_home_directories         | qetl_user_config_dir - yaml configuration  - /opt/qetl/users/qualys_user/qetl_home/config
    18	2021-05-28 01:26:03,900 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_user_home_directories         | qetl_user_cred_dir   - yaml credentials    - /opt/qetl/users/qualys_user/qetl_home/cred
    19	2021-05-28 01:26:03,900 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_user_home_directories         | qetl_user_bin_dir    - etl scripts         - /opt/qetl/users/qualys_user/qetl_home/bin
    20	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | load_etld_lib_config_settings_yaml       | etld_config_settings.yaml - kb_last_modified_after: default 
    21	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | load_etld_lib_config_settings_yaml       | etld_config_settings.yaml - kb_export_dir: default 
    22	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | load_etld_lib_config_settings_yaml       | etld_config_settings.yaml - host_list_vm_processed_after: default 
    23	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | load_etld_lib_config_settings_yaml       | etld_config_settings.yaml - host_list_payload_option: notags 
    24	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_kb_vars                       | knowledgeBase config - /opt/qetl/users/qualys_user/qetl_home/config/etld_config_settings.yaml
    25	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_kb_vars                       | kb_export_dir is direct from yaml
    26	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_kb_vars                       | kb_last_modified_after utc.now minus 7 days - 2021-05-21T00:00:00Z
    27	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_host_list_vars                | host list config - /opt/qetl/users/qualys_user/qetl_home/config/etld_config_settings.yaml
    28	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_host_list_vars                | host_list_vm_processed_after utc.now minus 7 days - 2021-05-27T00:00:00Z
    29	2021-05-28 01:26:03,902 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | setup_host_list_vars                | host_list_payload_option yaml - notags
    30	2021-05-28 01:26:03,906 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | spawn_etl_in_background                             | Job PID 247944 kb_etl_workflow job running in background.
    31	2021-05-28 01:26:03,907 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_start_wrapper                    | __start__ kb_etl_workflow ['/home/dgregory/opt/qetl/qetl_venv/bin/qetl_manage_user', '-u', '/opt/qetl/users/qualys_user', '-e', 'etl_knowledgebase: 20210528012603']
    32	2021-05-28 01:26:03,907 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_start_wrapper                    | data directory: /opt/qetl/users/qualys_user/qetl_home/data
    33	2021-05-28 01:26:03,907 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_start_wrapper                    | config file:    /opt/qetl/users/qualys_user/qetl_home/config/etld_config_settings.yaml
    34	2021-05-28 01:26:03,907 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_start_wrapper                    | cred yaml file: /opt/qetl/users/qualys_user/qetl_home/cred/.etld_cred.yaml
    35	2021-05-28 01:26:03,907 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_start_wrapper                    | cookie file:    /opt/qetl/users/qualys_user/qetl_home/cred/.etld_cookie
    36	2021-05-28 01:26:03,907 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_extract_wrapper                  | start knowledgebase_extract xml from qualys with kb_last_modified_after=2021-05-21T00:00:00Z
    37	2021-05-28 01:26:03,907 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | knowledgebase_extract                          | start
    38	2021-05-28 01:26:03,909 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | get_cred                            | Found your subscription credentials file:  /opt/qetl/users/qualys_user/qetl_home/cred/.etld_cred.yaml
    39	2021-05-28 01:26:03,909 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | get_cred                            |      username:         quays93
    40	2021-05-28 01:26:03,909 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | get_cred                            |      api_fqdn_server:  qualysapi.qg2.apps.qualys.com
    41	2021-05-28 01:26:03,909 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | get_cred                            |  ** Warning: Ensure Credential File permissions are correct for your company.
    42	2021-05-28 01:26:03,909 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | get_cred                            |  ** Warning: Credentials File: /opt/qetl/users/qualys_user/qetl_home/cred/.etld_cred.yaml
    43	2021-05-28 01:26:03,909 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | get_cred                            |  ** Permissions are: -rw------- for /opt/qetl/users/qualys_user/qetl_home/cred/.etld_cred.yaml
    44	2021-05-28 01:26:03,909 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | knowledgebase_extract                          | api call    - https://qualysapi.qg2.apps.qualys.com/api/2.0/fo/knowledge_base/vuln/
    45	2021-05-28 01:26:03,909 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | knowledgebase_extract                          | api options - {'action': 'list', 'details': 'All', 'show_disabled_flag': '1', 'show_qid_change_log': '1', 'show_supported_modules_info': '1', 'show_pci_reasons': '1', 'last_modified_after': '2021-05-21T00:00:00Z'}
    46	2021-05-28 01:26:03,909 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | knowledgebase_extract                          | cookie      - False
    47	2021-05-28 01:26:05,717 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | input file - https://qualysapi.qg2.apps.qualys.com/api/2.0/fo/knowledge_base/vuln/ size:  change time: 
    48	2021-05-28 01:26:05,718 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | output file - /opt/qetl/users/qualys_user/qetl_home/data/kb.xml size: 728.51 kilobytes change time: 2021-05-27 21:26:05 local timezone
    49	2021-05-28 01:26:05,718 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | knowledgebase_extract                          | end
    50	2021-05-28 01:26:05,718 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_extract_wrapper                  | end knowledgebase_extract xml from qualys
    51	2021-05-28 01:26:05,719 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_shelve_wrapper           | start kb_shelve xml to shelve
    52	2021-05-28 01:26:05,719 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_shelve_wrapper           | input file:  /opt/qetl/users/qualys_user/qetl_home/data/kb.xml
    53	2021-05-28 01:26:05,719 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_shelve_wrapper           | output file: /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve
    54	2021-05-28 01:26:05,719 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_shelve                           | start
    55	2021-05-28 01:26:05,744 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_dbm_info                        | dbm type - dbm.gnu - /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve
    56	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_shelve                           | count qualys qid added to shelve: 137 for /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve
    57	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | input file - /opt/qetl/users/qualys_user/qetl_home/data/kb.xml size: 728.51 kilobytes change time: 2021-05-27 21:26:05 local timezone
    58	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_dbm_info                        | dbm type - dbm.gnu - /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve
    59	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | output file - /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve size: 632.00 kilobytes change time: 2021-05-27 21:26:05 local timezone
    60	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_shelve                           | end
    61	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_shelve_wrapper           | end   kb_shelve xml to shelve
    62	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_json_wrapper                  | start kb_load_json transform Shelve to JSON
    63	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_json_wrapper                  | input file:   /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve
    64	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_json_wrapper                  | output File:  /opt/qetl/users/qualys_user/qetl_home/data/kb.json
    65	2021-05-28 01:26:05,815 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_load_json                             | start
    66	2021-05-28 01:26:05,840 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_load_json                             | count qid loaded to json: 137
    67	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | input file - /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve size: 632.00 kilobytes change time: 2021-05-27 21:26:05 local timezone
    68	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_dbm_info                        | dbm type - dbm.gnu - /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve
    69	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | output file - /opt/qetl/users/qualys_user/qetl_home/data/kb.json size: 645.81 kilobytes change time: 2021-05-27 21:26:05 local timezone
    70	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_load_json                             | end
    71	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_json_wrapper                  | end   kb_load_json transform Shelve to JSON
    72	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_csv_wrapper                   | start kb_load_csv - shelve to csv
    73	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_csv_wrapper                   | input file:   /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve
    74	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_csv_wrapper                   | output file: /opt/qetl/users/qualys_user/qetl_home/data/kb.csv
    75	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_csv_wrapper                   | output file: /opt/qetl/users/qualys_user/qetl_home/data/kb_cve_qid_map.csv  cve -> qid map in csv format
    76	2021-05-28 01:26:05,841 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_create_csv_from_shelve           | start
    77	2021-05-28 01:26:05,864 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_create_csv_from_shelve           | count rows written to csv: 137
    78	2021-05-28 01:26:05,864 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | input file - /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve size: 632.00 kilobytes change time: 2021-05-27 21:26:05 local timezone
    79	2021-05-28 01:26:05,864 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_dbm_info                        | dbm type - dbm.gnu - /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve
    80	2021-05-28 01:26:05,864 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | output file - /opt/qetl/users/qualys_user/qetl_home/data/kb.csv size: 387.65 kilobytes change time: 2021-05-27 21:26:05 local timezone
    81	2021-05-28 01:26:05,864 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_create_csv_from_shelve           | end
    82	2021-05-28 01:26:05,867 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_create_cve_qid_shelve            | count rows written to cve to qid shelve: 334
    83	2021-05-28 01:26:05,868 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | input file - /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve size: 632.00 kilobytes change time: 2021-05-27 21:26:05 local timezone
    84	2021-05-28 01:26:05,868 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_dbm_info                        | dbm type - dbm.gnu - /opt/qetl/users/qualys_user/qetl_home/data/kb_shelve
    85	2021-05-28 01:26:05,868 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | output file - /opt/qetl/users/qualys_user/qetl_home/data/kb_cve_qid_map_shelve size: 44.00 kilobytes change time: 2021-05-27 21:26:05 local timezone
    86	2021-05-28 01:26:05,868 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_csv_wrapper                   | end   kb_load_csv - shelve to csv
    87	2021-05-28 01:26:05,868 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_cve_qid_csv_wrapper           | start kb_load_cve_qid_csv transform Shelve to CSV
    88	2021-05-28 01:26:05,868 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_cve_qid_csv_wrapper           | input file:  /opt/qetl/users/qualys_user/qetl_home/data/kb_cve_qid_map_shelve
    89	2021-05-28 01:26:05,868 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_cve_qid_csv_wrapper           | output file: /opt/qetl/users/qualys_user/qetl_home/data/kb_cve_qid_map.csv
    90	2021-05-28 01:26:05,868 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_cve_qid_csv_report               | Start
    91	2021-05-28 01:26:05,869 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_cve_qid_csv_report               | Count of CVE rows written: 334
    92	2021-05-28 01:26:05,869 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_cve_qid_csv_report               | End
    93	2021-05-28 01:26:05,869 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_cve_qid_csv_wrapper           | end   kb_load_cve_qid_csv transform Shelve to CSV
    94	2021-05-28 01:26:05,869 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_sqlite_wrapper                | start kb_load_sqlite transform Shelve to Sqlite3 DB
    95	2021-05-28 01:26:05,869 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_sqlite_wrapper                | input file:   /opt/qetl/users/qualys_user/qetl_home/data/kb.csv
    96	2021-05-28 01:26:05,869 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_sqlite_wrapper                | output file: /opt/qetl/users/qualys_user/qetl_home/data/kb_load_sqlite.db
    97	2021-05-28 01:26:05,869 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_load_sqlite                           | start
    98	2021-05-28 01:26:05,884 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | bulk_insert_csv_file                | Count rows added to table: 137
    99	2021-05-28 01:26:05,884 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | input file - /opt/qetl/users/qualys_user/qetl_home/data/kb.csv size: 387.65 kilobytes change time: 2021-05-27 21:26:05 local timezone
   100	2021-05-28 01:26:05,884 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | log_file_info                       | output file - /opt/qetl/users/qualys_user/qetl_home/data/kb_load_sqlite.db size: 520.00 kilobytes change time: 2021-05-27 21:26:05 local timezone
   101	2021-05-28 01:26:05,884 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_load_sqlite                           | end
   102	2021-05-28 01:26:05,884 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_to_sqlite_wrapper                | end   kb_load_sqlite transform Shelve to Sqlite3 DB
   103	2021-05-28 01:26:05,884 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_distribution_wrapper             | start kb_distribution
   104	2021-05-28 01:26:05,884 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_dist                             | start
   105	2021-05-28 01:26:05,884 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | copy_results_to_external_target     | no actions taken.  etld_config_settings.yaml kb_export_dir set to: default
   106	2021-05-28 01:26:05,885 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_dist                             | end
   107	2021-05-28 01:26:05,885 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_distribution_wrapper             | end   kb_distribution
   108	2021-05-28 01:26:05,885 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_end_wrapper                      | runtime for kb_etl_workflow in seconds: 1.9780801669985522
   109	2021-05-28 01:26:05,885 | INFO     | etl_knowledgebase: 20210528012603    | dgregory        | kb_end_wrapper                      | __end__ kb_etl_workflow ['/home/dgregory/opt/qetl/qetl_venv/bin/qetl_manage_user', '-u', '/opt/qetl/users/qualys_user', '-e', 'etl_knowledgebase: 20210528012603']
```

### Review ETL KnowledgeBase Data

```bash
(qetl_venv) qualysetl@ubuntu:/opt/qetl/users/qualys_user/qetl_home/data$ cd /opt/qetl/users/qualys_user/qetl_home/data/
(qetl_venv) qualysetl@ubuntu:/opt/qetl/users/qualys_user/qetl_home/data$ ls | nl
     1	kb.csv
     2	kb_cve_qid_map.csv
     3	kb_cve_qid_map_shelve
     4	kb.json
     5	kb_shelve
     6	kb_load_sqlite.db
     7	kb.xml
(qetl_venv) qualysetl@ubuntu:/opt/qetl/users/qualys_user/qetl_home/data$ head -20 kb.json
[{
    "QID": "238914",
    "VULN_TYPE": "Vulnerability",
    "SEVERITY_LEVEL": "4",
    "TITLE": "Red Hat Update for Red Hat JBoss Enterprise Application Platform 7.3.4 (RHSA-2020:5341)",
    "CATEGORY": "RedHat",
    "LAST_SERVICE_MODIFICATION_DATETIME": "2021-05-21T07:20:40Z",
    "PUBLISHED_DATETIME": "2020-12-11T12:36:56Z",
    "PATCHABLE": "1",
    "SOFTWARE_LIST": {
        "SOFTWARE": [
            {
                "PRODUCT": "jboss_enterprise_application_platform",
                "VENDOR": "redhat"
            },
```

## License
[Apache License](http://www.apache.org/licenses/LICENSE-2.0)

    Copyright 2021  David Gregory and Qualys Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

## ChangeLog
Beginning with 0.80 a change log will be maintained here.

Version | Date | Description of Changes
---------- | ------ | -----------
0.80 | TBD | Perfect
