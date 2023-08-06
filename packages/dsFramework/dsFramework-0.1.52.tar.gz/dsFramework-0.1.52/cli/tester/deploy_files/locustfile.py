from locust import HttpUser, task
import pandas as pd
import numpy as np

jwtToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImI2ZjhkNTVkYTUzNGVhOTFjYjJjYjAwZTFhZjRlOGUwY2RlY2E5M2QiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiIxMDQyNTE5MDYyNzcwLXJnaGJzMWllZDhrbm83bDAwbWxua281cjdzZ2plYTJvLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXpwIjoiand0LXNjb29wcy1jbGFzc2lmaWNhdGlvbkBkb3ppLXN0Zy1kcy1hcHBzLTEuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJlbWFpbCI6Imp3dC1zY29vcHMtY2xhc3NpZmljYXRpb25AZG96aS1zdGctZHMtYXBwcy0xLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTYyNTMwNTYzNSwiaWF0IjoxNjI1MzAyMDM1LCJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJzdWIiOiIxMTIwNDkzNDcxMjg1ODg2ODMzNDEifQ.BwrXdbIfzEVak1yvoVvp_aVskHLbPDPDm2Mr1uyh3QIYr2Crd_r4ROAXYaW3kSUi9mRlt7_KY6ovQ8RCK24mAuYGFvr3Kyk4IFbOFNUzMb3xCZxRxsfhtA-Djy16XA50B6tieQkptFV2A6eXnT1mo3tIaNu0NsJgqbZkiJPmHsMBYkDwGn_IwC8ooJeI8JRj55liLwpjVkoU0gCbX7ohL7gz3gV8dxYEkywLOEDquJJM0TcISgQ1FqKcS9h33GQ9cjB9xamlulfUeVQlDDXoceoIcUpD-ySNTmq_wBEyX3dlu4f9YF8PA13M5E0U2fpeyivPp_mSPcKNgMzz0JbUOQ'
global_headers = {
    'x-token': 'fake-super-secret-token',
    'Authorization': 'Bearer ' + jwtToken
}

class payloadUser(HttpUser):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.df = pd.read_csv("sample.csv", sep='\t')
		self.df.replace(np.nan, '', regex=True)

	def get_random_row(self):
		s = self.df.sample().to_dict('list')
		d = dict((k.lower(), v[0]) for k, v in s.items())
		return d

	@task
	def get_diagnosis_with_valid_payload(self):
		headers = {"Content-Type": "application/json; charset=UTF-8", **global_headers}
		payload = self.get_random_row()
		self.client.post("/predict", json=payload, headers=headers)


# how to run
# --host - Host to load test in the following format: http://example.com
# --users - Number of concurrent Locust users
# --spawn-rate - The rate per second in which users are spawned
# locust -f locustfile.py --host={your-host} --users={number-of-users} --spawn-rate={your-spawn-rate}
