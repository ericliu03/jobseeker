'''
@author: Xinyue Wang
Search candidates for companies
'''
import random
import json

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from faker import Factory


class SearchCandidates(object):
    """search candidate with queries"""

    def __init__(self):
        self.id = ""
        self.name = ""
        self.email = ""
        self.phone = ""
        self.skills = []
        self.education = ""
        self.es = Elasticsearch()
        self.skill_pool = []
        self.schema = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "index_analyzer": {
                            "type": "standard",
                        },
                        "search_analyzer": {
                            "tokenizer": "standard",
                            "filter": ["standard", "lowercase", "stop", "asciifolding", "porter_stem"]
                        }
                    },

                },
                "filter": {
                    "my_ascii_folding": {
                        "type": "asciifolding",
                        "preserve_original": True
                    }
                }

            },
            "mappings": {
                "candidates": {
                    "properties": {
                        "id": {"type": "string", "index": "not_analyzed"},
                        "name": {"type": "string", "index": "not_analyzed"},
                        "email": {"type": "string", "index": "not_analyzed"},
                        "phone": {"type": "string", "index": "analyzed"},
                        "skills": {"type": "string"},
                        "education": {"type": "string", "index": "not_analyzed"},
                        "job_exp": {"type": "long", "index": "not_analyzed"}
                    }
                }
            }
        }

    def set_up_es(self, candidate_info):
        """set up elastic search and bulk load"""
        try:
            self.es.indices.delete(index=u"i_candidates")
        except NameError:
            self.es.indices.create(index=u"i_candidates", body=self.schema)
        j = 0
        actions = []
        while j in range(0, len(candidate_info)):
            action = self.format_d_action("i_candidates", "candidates", j, candidate_info[j])
            actions.append(action)
            j += 1
        helpers.bulk(self.es, actions=actions, index="i_candidates", doc_type="candidates", refresh=True)

    def format_d_action(self, index_name, type_name, uid, data):
        """actions for bulk loads"""
        d_action = {"_index": index_name, "_type": type_name, "_id": uid, "_source": data}
        return d_action

    def total(self):
        """return all results, used when no search constraint is specified"""
        res = self.es.search(index="i_candidates", body={"query": {"match_all": {}}})
        result = []
        for i in range(len(res["hits"]["hits"])):
            result += [res["hits"]["hits"][i]['_source']]
        return result

    def output(self, multiword):
        """output for search results, top 20 chosen"""
        result = []
        for i in range(0, min([20, len(multiword["hits"]["hits"])])):
            result += [{"name": multiword["hits"]["hits"][i]["_source"]["name"],
                        "email": multiword["hits"]["hits"][i]["_source"]["email"],
                        "phone": multiword["hits"]["hits"][i]["_source"]['phone'],
                        "skills": multiword["hits"]["hits"][i]["_source"]['skills'],
                        "education": multiword["hits"]["hits"][i]["_source"]['education'],
                        "job_exp": multiword["hits"]["hits"][i]["_source"]['job_exp']}]
        if len(result) == 0:
            return None
        else:
            return result

    def is_empty(self, l):
        """whether an input is empty"""
        return len(l) == 0 or l == [""]

    def search(self, skills, education, job_exp):
        """skills = skills, education = education, job_exp = job_exp, search with job experience filter"""
        if self.is_empty(skills) and self.is_empty(education):
            return self.total()
        params = [skills] + [education]
        query_words = []
        for i in range(len(params)):
            if not self.is_empty(params[i]):
                query_words += params[i][0].lower().split(" ")
        if self.is_empty(params[0]) and (self.is_empty(params[1]) == False):
            fields = ["education"]
        elif self.is_empty(params[1]) and (self.is_empty(params[0]) == False):
            fields = ["skills"]
        else:
            fields = ["skills", "education"]
        print query_words
        print fields
        "default min and max years of job experience"
        min_job_exp = 0
        max_job_exp = 20
        if job_exp[0] != "":
            min_job_exp = int(job_exp[0])
        if job_exp[1] != "":
            max_job_exp = int(job_exp[1])
        query = {
            "size": 100,
            "query": {
                "multi_match": {
                    "query": query_words,
                    "type": "best_fields",
                    "fields": fields,
                    "operator": "and"
                },
            },
            "filter": {
                "range": {
                    "job_exp": {
                        "gte": min_job_exp,
                        "lte": max_job_exp
                    }
                }
            }
        }
        multiword = self.es.search(index="i_candidates", doc_type="candidates", body=query)
        return self.output(multiword)


class CandidateDataGenerator(object):
    """generate candidate information since personal data(personal info, resume, etc) is inaccessible due to privacy"""

    def __init__(self, user_nums):
        self.user_num = user_nums
        self.skill_pool = []
        self.education_level = ['bachelor', 'master', 'phd']
        f = open('list.txt', 'r')
        for line in f:
            self.skill_pool += line.splitlines()
        f.close()
        self.record = []
        self.fake = Factory.create()
        self.output_format = {"data": self.record}

    def generate_edu_level(self, edu_level):
        """random assign education level, Bachelor, Masters or PhD"""
        return self.education_level[edu_level]

    def generate_skills(self, num_skills):
        """random choose a certain number of skills according to parameter num_skills"""
        index_list = random.sample(xrange(0, len(self.skill_pool) - 1), num_skills)
        result = []
        for i in index_list:
            result += [self.skill_pool[i]]
        return result

    def generate_record(self):
        """combine all the generated information into a record"""
        for i in range(self.user_num):
            skills = self.generate_skills(random.randint(1, 10))
            job_exp = random.randint(0, 20)
            name = self.fake.name()
            if "PhD" in name:
                "generated name with PhD title, auto-assign PhD education level"
                edu_level = self.generate_edu_level(2)
            else:
                edu_level = self.generate_edu_level(random.randint(0, 2))
            email = self.fake.email()
            phone_number = self.fake.phone_number()
            self.record += [{"id": str(i), "name": name, "email": email, "phone": phone_number, "skills": skills,
                             "education": edu_level, "job_exp": job_exp}]


if __name__ == '__main__':
    """for writing unit tests, set up data and query for test searches"""
    si = SearchCandidates()
    try:
        # f = open('users.txt', 'r')
        # candidate_data = json.loads(f.read())
        # record = candidate_data["data"]
        # si.set_up_es(record)
        print 12,si.search(["java"], [""], ["", ""])
        # f.close()
    except IOError:
        pass
        # print "First time to generate data...."
        # g = CandidateDataGenerator(1000)
        # g.generate_record()
        # si.set_up_es(g.record)
        # output = open('output.txt', 'wb')
        # json_output = json.dumps(g.output_format, indent=4)
        # json_output = unicode(json_output, 'utf-8')
        # output.write(json_output)
