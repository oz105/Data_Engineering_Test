import json


class Job:

    job_counter = 0

    def __init__(self, job_title, country, city, job_description):
        self.num_of_job = Job.job_counter
        self.job_title = job_title
        self.country = country
        self.city = city
        self.job_description = job_description
        Job.job_counter += 1

    def to_dict(self):
        res = {'job_title': self.job_title,
               'country': self.country,
               'city': self.city,
               'job_description': self.job_description
               }
        return res

    def __str__(self):
        return str(self.to_dict())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
