from django.db import models


class Candidate(models.Model):
    # example
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=200, blank=False, null=True)

    name = models.CharField(max_length=200, blank=False)
    email = models.CharField(max_length=200, blank=False, null=True, default='')
    phone = models.CharField(max_length=200, blank=True, null=True)
    skills = models.CharField(max_length=200, blank=True, null=True, default='')
    education = models.CharField(max_length=200, blank=True, null=True, default='')
    job_exp = models.CharField(max_length=200, blank=True, null=True, default='')

    query_string = models.CharField(max_length=200, blank=True, null=True, default='')
    location = models.CharField(max_length=200, blank=True, null=True, default='')
    job_type = models.CharField(max_length=200, blank=True, null=True, default='')
    company = models.CharField(max_length=200, blank=True, null=True, default='')
    search_range = models.CharField(max_length=200, blank=True, null=True, default='')
    use_history = models.CharField(max_length=200, blank=True, null=True, default='False')

    def get_search_info(self):
        dic = {
            'query_string': self.query_string,
            'location': self.location,
            'job_type': self.job_type,
            'company': self.company,

            'skills': self.skills,
            'education': self.education,
            'search_range': self.search_range,
        }
        return dic.iteritems()

    def save_search_info(self, query_string, location, job_type, company, search_range):
        self.query_string = query_string
        self.location = location
        self.job_type = job_type
        self.company = company
        self.search_range = search_range

    def get_create_info(self):
        dic = {
            'name': self.name,
            'email': self.email,
        }
        return dic.iteritems()

    def get_profile_info(self):
        dic = {
            'name': self.name,
            'email': self.email,
            'skills': self.skills,
            'education': self.education,
            'phone': self.phone,
            'job_exp': self.job_exp,
        }
        return dic.iteritems()

    def save_profile_info(self, name, email, skills, education, phone, job_exp):
        self.name = name
        self.email = email
        self.skills = skills
        self.education = education
        self.phone = phone
        self.job_exp = job_exp

    def set_info(self, key, value):
        if key == 'user_id':
            self.user_id = value
        if key == 'name':
            self.name = value
        elif key == 'email':
            self.email = value
        elif key == 'phone':
            self.phone = value
        elif key == 'skills':
            self.skills = value
        elif key == 'education':
            self.education = value
        elif key == 'job_exp':
            self.job_exp = value

        elif key == 'query_string':
            self.query_string = value
        elif key == 'location':
            self.location = value
        elif key == 'job_type':
            self.job_type = value
        elif key == 'company':
            self.company = value
        elif key == 'search_range':
            self.search_range = value
        elif key == 'use_history':
            self.use_history = value
        else:
            pass  # error

    def __unicode__(self):
        return 'Id: ' + str(self.id) + ' Name: ' + self.name


class HitHistory(models.Model):
    candidate = models.ForeignKey(Candidate)
    job_id = models.CharField(max_length=200, blank=False)
    hits = models.IntegerField(default=0)
    hit_time = models.DateField(auto_now=True)

    def get_record(self):
        return {'job_id': self.job_id,
                'hits': self.hits,
                'hit_time': self.hit_time,
        }

