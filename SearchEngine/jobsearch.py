'''
@author: Kechen
'''
import time
import datetime

from elasticsearch import Elasticsearch
from geopy.geocoders import Nominatim


class jobsearch():
    def __init__(self):
        self.es = Elasticsearch(timeout=30)

    def create_job_index(self, index_name):
        '''Create index, including snowball analyzer, lowercase analyzer, bigram analyzer.'''
        job_schema = {"mappings":
                          {"job":
                               {"properties":
                                    {
                                        # "skills": {"type":"string", "index": "not_analyzed"},
                                        "plus": {"type": "string", "index": "not_analyzed"},
                                        "education": {"analyzer": "standard", "type": "string"},
                                        "text": {"type": "string", "analyzer": "english",
                                                 "fields": {
                                                     "shingles": {
                                                         "type": "string",
                                                         "analyzer": "my_shingle_analyzer"
                                                     }
                                                 }
                                        },
                                        "job_type": {"type": "string", 'analyzer': 'lower_case'},
                                        "job_title": {"analyzer": "lower_case", "type": "string",
                                                      "fields": {
                                                          "shingles": {
                                                              "type": "string",
                                                              "analyzer": "my_shingle_analyzer"
                                                          }
                                                      }
                                        },
                                        "company": {"analyzer": "standard", "type": "string"},
                                        "city": {"analyzer": "standard", "type": "string"},
                                        "state": {"analyzer": "standard", "type": "string"},
                                        "country": {"analyzer": "standard", "type": "string"},
                                        "date": {"index": "not_analyzed", "type": "string"},
                                        "location": {"type": "geo_point"},
                                        "url": {"index": "not_analyzed", "type": "string"},
                                    }}},
                      "settings": {
                          "analysis": {
                              "filter": {
                                  "my_shingle_filter": {
                                      "type": "shingle",
                                      "min_shingle_size": 2,
                                      "max_shingle_size": 2,
                                      "output_unigrams": False
                                  }
                              },
                              "analyzer": {
                                  "my_analyzer": {
                                      "type": "snowball",
                                      "language": "English"
                                  },
                                  "lower_case": {
                                      "type": "custom",
                                      "tokenizer": "keyword",
                                      "filter": "lowercase"
                                  },
                                  "my_shingle_analyzer": {
                                      "type": "custom",
                                      "tokenizer": "standard",
                                      "filter": [
                                          "lowercase",
                                          "my_shingle_filter"
                                      ]
                                  }
                              }
                          }
                      }}
        job_index = self.es.indices.create(index=index_name, body=job_schema)
        return job_schema

    def create_index(self, index_name='job_index'):
        '''If this index exists, delete it. Or create a new index using this index name'''
        if self.es.indices.exists(index_name):
            res = self.es.indices.delete(index=index_name)
        self.create_job_index(index_name)

    def bulk_load(self, filename="test123456.txt", index_name='job_index', type_name='job'):
        '''Import data into index'''
        bulk_data = []
        file = open(filename)
        i = 1
        for line in file:
            bulk_data.append(self.format_d_action(index_name, type_name, i))
            bulk_data.append(line)
            i = i + 1
        res = self.es.bulk(index=index_name, body=bulk_data, refresh=True)
        file.close()
        print 'load finish!'

    def format_d_action(self, index_name, type_name, uid):
        '''Set bulk load json'''
        d_action = {"index": {"_index": index_name, "_type": type_name, "_id": uid}}
        return d_action

    def get_geocoordinate(self, address):
        '''Get latitude and longitude of a city'''
        geolocator = Nominatim()
        try:
            location = geolocator.geocode(address, timeout=10)
        except Exception, e:
            print e
        if location:
            return ((location.latitude, location.longitude))
        else:
            return 'nothing'


    def q_mw(self, field, string):
        '''This is just a test'''
        result = ''
        queryBody = {
            "query": {
                "multi_match": {"query": "Engineer Intern hello",
                                "fields": ["text.shingles" + "^2", "job_title.shingles"]}
            },
            "highlight": {
                "fields": {
                    field: {}
                }
            },
            "size": 10
        }
        start = time.clock()
        res = self.es.search('job_index', 'job', queryBody)
        end = time.clock()
        print res
        print res['hits']['total']

    def main_search(self, query_stat, location, education_list, plus_list, job_type, company, range, historyflag,
                    history_data,
                    field0='job_title', field1='text', field2='city', field3='state', field4='country',
                    field5='education', field6='skills', field7='plus',
                    field8='job_type', field9='company'):
        '''The main search, user should at least input query statement and location.
            education level top1
            union set of plus skills
            job_type the nearest 10 times search
            location top1'''

        if location == "":
            location = 'us'
            city_cord = "nothing"
        else:
            city_cord = self.get_geocoordinate(location)  # get city cooridinate

        must_list = [{"multi_match": {"query": query_stat,
                                      "fields": [field0 + "^2", field1]}}
        ]
        should_list = [
            {"multi_match": {"query": query_stat,
                             "fields": [field0 + ".shingles" + "^2", field1 + ".shingles"]}},
            {"multi_match": {"query": location,
                             "type": "cross_fields",
                             "fields": [field2, field3, field4],
                             "operator": "and"}}]
        must_not_list = []
        geo_filter = {}

        if company != '':
            must_list.append({"fuzzy": {field9: company}})
        if job_type != '':
            must_list.append({"match": {field8: job_type}})
        if education_list != []:
            must_list.append({"terms": {field5: education_list,
                                        "minimum_should_match": 1}})
        if city_cord != "nothing" and range != "":
            geo_filter = {
                "geo_distance": {
                    "distance": range + 'km',
                    "location": str(city_cord[0]) + "," + str(city_cord[1])
                }}
        print city_cord
        if city_cord != "nothing" and range == "":
            geo_filter = {
                "geo_distance": {
                    "distance": '25km',
                    "location": str(city_cord[0]) + "," + str(city_cord[1])
                }}

        if plus_list:
            should_list.append({"terms": {field7: plus_list,
                                          "minimum_should_match": 1}})
        queryBody = {
            'query': {
                "bool": {
                    "must": must_list,
                    # "must_not": [
                    # { "terms" : {field6 : skills_list,
                    # "minimum_should_match" : 1}}
                    #                                   ],
                    "should": should_list,
                    #                      "minimum_should_match" : 1
                }
            },
            "filter": geo_filter,
            "highlight": {
                "pre_tags": ["<b>"],
                "post_tags": ["</b>"],
                "fields": {
                    'text': {},
                }
            },
            "size": 15
        }

        if historyflag == 'True':
            print '123123'
            historydic = self.get_historydat(history_data)
            history_plus = historydic["plus"]
            history_location = historydic["location"]
            history_job_type = historydic["job_type"]
            history_education = historydic["education"]
            rescoreQueryBody = {
                "window_size": 50,
                "query": {
                    'rescore_query': {
                        "bool": {
                            "must": [{"multi_match": {"query": query_stat,
                                                      "fields": [field0 + "^2", field1]}},
                                     {"multi_match": {"query": 'waltham',
                                                      "type": "cross_fields",
                                                      "fields": [field2, field3, field4],
                                                      "operator": "and"}},
                                     {"match": {field8: history_job_type}},
                                     {"terms": {field5: history_education,
                                                "minimum_should_match": 1}}],
                            "should": [{"multi_match": {"query": query_stat,
                                                        "fields": ["job_title" + ".shingles" + "^2",
                                                                   "text" + ".shingles"]}},
                                       {"terms": {"plus": history_plus,
                                                  "minimum_should_match": 1}}]
                        }
                    },
                    "query_weight": 1.0,
                    "rescore_query_weight": 0.2}}
            queryBody['rescore'] = rescoreQueryBody


        # print json.dumps(queryBody,indent=4)
        start = time.clock()
        res = self.es.search('job_index', 'job', queryBody)
        end = time.clock()

        hits = res['hits']['total']

        # print json.dumps(res,indent=4)
        # print hits
        return self.process_result(res, end - start)

    def process_result(self, search_result, time):
        '''transform elasticsearch result to dictionary'''
        result_list = search_result['hits']['hits']
        processed = []
        for each in result_list:
            each['_source']['job_id'] = each['_id']
            each['_source']['snippet'] = '\n'.join(each['highlight']['text'])
            each['_source']['education'] = ', '.join(each['_source']['education'])
            each['_source']['skills'] = ', '.join(each['_source']['plus'])
            print each['_source']['plus']
            processed.append(each['_source'])
        if len(processed) == 0:
            return None
        return processed, time

    def get_job(self, job_id):
        queryBody = {
            "query": {
                "match": {
                    '_id': job_id
                }
            }}
        res = self.es.search('job_index', 'job', queryBody)

        return res['hits']['hits'][0]['_source']

    def get_historydat(self, history_list):
        # top three plus skills
        # union set of education level
        # job_type the nearest 10 times search
        # location top1
        educationset = set()
        plusset = set()
        citydic = {}
        job_typedic = {'fulltime': 0, 'internship': 0}
        educationdic = {}
        for hit in history_list:
            # only keep historical data for twenty days recently
            if (datetime.datetime.now().date() - hit['hit_time']).days < 20:
                job = self.get_job(int(hit['job_id']))
                plus = job['plus']
                education = job['education'][0]
                job_type = job['job_type']
                city = job['city']
                for edu in education:
                    educationset.add(edu)
                for skill in plus:
                    plusset.add(skill)
                job_typedic[job_type] += 1
                if educationdic.has_key(education):
                    educationdic[education] += 1
                else:
                    educationdic[education] = 1
                if citydic.has_key(city):
                    citydic[city] += 1
                else:
                    citydic[city] = 1
                    # state = job['state']
                    # country = job['country']
        citylist = sorted(citydic.items(), key=lambda d: d[1], reverse=True)
        edlist = sorted(educationdic.items(), key=lambda d: d[1], reverse=True)
        job_type = job_typedic['fulltime'] > job_typedic['internship'] and 'fulltime' or 'internship'
        dic = {'plus': list(plusset), 'education': [edlist[0][0]], 'job_type': job_type, 'location': citylist[0][0]}
        # dic = {'plus':["development",
        # "data",
        # "testing",
        #                        "design",
        #                        "software"], 'education':['bachelor'],'job_type':'internship','location':'waltham'}


        return dic

    def recommend(self, history_list):
        '''recommend search'''
        historydic = self.get_historydat(history_list)
        history_plus = historydic["plus"]
        history_location = historydic["location"]
        history_job_type = historydic["job_type"]
        history_education = historydic["education"]
        query_stat = ''
        for skill in history_plus:
            query_stat = query_stat + skill + ' '
        # print query_stat
        queryBody = {
            'query': {
                "bool": {
                    "must": [{"multi_match": {"query": query_stat,
                                              "fields": ["job_title" + "^2", "text"]}},
                             {"multi_match": {"query": history_location,
                                              "type": "cross_fields",
                                              "fields": ["city", "state", "country"],
                                              "operator": "and"}},
                             {"match": {'job_type': history_job_type}},
                             {"terms": {'education': history_education,
                                        "minimum_should_match": 1}}]
                }
            },
            "size": 20
        }
        start = time.clock()
        res = self.es.search('job_index', 'job', queryBody)
        end = time.clock()

        ids = [job['_id'] for job in res['hits']['hits']]
        scores = [job['_score'] for job in res['hits']['hits']]
        recdic = dict((key, value) for key, value in zip(ids, scores))

        # print json.dumps(res,indent=4)
        # print hits

        return self.process_result(res, end - start)


if __name__ == '__main__':
    my_query = jobsearch()
    # my_query.create_index()
    # my_query.bulk_load()
    # my_query.q_mw('country', 'US')
    my_query.main_search('software', 'newton,ma', ['bachelor'], [], 'fulltime', '', '200', 'False',
                         my_query.get_historydat(1))
    #    my_query.recommend('java developer', ['master'], 'waltham', 'intern', ['java', 'python'])
    #    print my_query.get_job(1)
    #    print my_query.get_historydat(1)
    #    a={'job_type': 'internship', 'education': [u'bachelor', u'master'], 'plus': [u'web', u'prioritizing', u'applications', u'communication', u'support', u'processing', u'training', u'presentations', u'collaboration', u'metrics', u'analytics', u'interpersonal', u'supervision', u'internet', u'analytical', u'writing', u'data', u'email'], 'location': u'Miami'}
    #    print my_query.recommend(a)
    #    print set(['s','s','c'])