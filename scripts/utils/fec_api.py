from requests import Request, Session
from scripts.settings import API_KEY
from urllib.parse import urljoin
BASE_URL = "http://api.open.fec.gov/v1/"

def base_request(api_key = API_KEY):
  req = Request('GET')
  req.params = {'api_key': API_KEY, 'per_page': 100}
  req.url = BASE_URL
  return req

def get_candidate(cand_id):
  req = base_request()
  req.url = urljoin(req.url, 'candidate/' + cand_id)
  return send(req)

def get_committee_totals(comm_id):
  pass

def get_candidate_committees(cand_id):
  pass


def send(req_obj):
  s = Session()
  resp = s.send(req_obj.prepare())
  return resp
