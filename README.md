# Predictive NBA Analysis

### Data Crawler
Generates JSON files for statistics of every game in a specified season
> python match_generator.py --league nba --seasons 2003-2004


### Data Schema
To generate postgreSQL tables run:
> python -m data-schema.create_db

To load tables with the JSON data run:
> python -m data-schema.loader


### Sources
Majority of data crawler and data schema code is a modified version of:
* https://github.com/FranGoitia/basketball_reference 
* https://github.com/FranGoitia/basketball-analytics