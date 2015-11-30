from SearchEngine import jobsearch

# upload data from file to elasticsearch server
ES = jobsearch.jobsearch()
ES.create_index()
ES.bulk_load(filename='SearchEngine/job_data.txt')
