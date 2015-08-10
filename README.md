## datahoarder/fec_api_data


Exploring the FEC API Data

[Sunlight Foundation tutorial](https://sunlightfoundation.com/blog/2015/07/08/openfec-makes-campaign-finance-data-more-accessible-with-new-api-heres-how-to-get-started/)


- base_url: http://api.open.fec.gov/v1
- candidate endpoint: /candidate
- candidates search: /candidates/search

Sample calls:

### Search for Obama:

- http://api.open.fec.gov/v1/candidates/search?api_key=API_KEY&q=obama


### History of Obama's candidate ID: H0IL01087

- http://api.open.fec.gov/v1/candidate/H0IL01087/history?api_key=API_KEY


### Declared candidates in 2014 cycle who have raised at least $5,000

http://api.open.fec.gov/v1/candidates?api_key=API_KEY&cycle=2014&candidate_status=C


### Candidate principal committees

http://api.open.fec.gov/v1/candidate/H0IL01087/committees?api_key=API_KEY&cycle=2000&designation=P

### Candidate principal, House committees

http://api.open.fec.gov/v1/candidate/H0IL01087/committees?api_key=API_KEY&cycle=2000&committee_type=H&designation=P


### Committee totals (all cycles)

http://api.open.fec.gov/v1/committee/C00347583/totals?api_key=API_KEY

### Committee reports

http://api.open.fec.gov/v1/committee/C00347583/reports?api_key=API_KEY
