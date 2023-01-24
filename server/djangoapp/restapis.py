import requests
import json
from datetime import datetime
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions



#Getting json data from API
def get_request(url, **kwargs):
    #print("GET from {} ".format(url))
    try:
        '''
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
        '''
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


#Getting reviews
def get_review(url, dealer):
    review=[]
    result= get_request(url, dealership=str(dealer))['reviews'][0]
    if result:
        review = DealerReview(dealership=result['dealership'],name=result['name'],purchase=result['purchase'],review=result['review'],
                                           purchase_date=result['purchase_date'],car_make=result['car_make'],car_model=result['car_model'],
                                            car_year=result['car_year'],sentiment=analyze_review_sentiments(result['review']),id=result['id'])
  

    return review
 
#Analyzing dealer review(AI)
def analyze_review_sentiments(dealerreview):
    url = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/a5c10170-f890-4b15-803b-11625ae00e32'
    api_key = '7dHR8vRYVm5F-K8Z10h4ME9mZlHhSqTTiQEsfuG0jwbo'
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    response = natural_language_understanding.analyze( text=dealerreview,features=Features(sentiment=SentimentOptions(targets=[dealerreview]))).get_result() 
    label=json.dumps(response, indent=2) 

    label = response['sentiment']['document']['label'] 

    return label


#dealers by state
def get_dealers_for_st(url, st):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, st=st)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

#dealers by id
def get_dealers_for_id(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

#Get all dealers
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            dealer_doc = dealer['doc']
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


'''
urld = "https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/review-package/get-reviews"
review=get_review(urld,29)
print(review.car_make)
'''
'''
urld = "https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/dealership-package/get-dealership-async"
details = get_dealers_for_st(urld,"TX")
for detail in details:

    print(detail.address)
'''

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
'''
json_={}
review=DealerReview(
car_make= "GMC",
name="Henry",
dealership= 45,
review= "Great Service",
purchase="True")
json_['review']= review
json_payload = DealerReview.to_json(json_)
'''

'''
url="https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/review-package/post-review"

r= post_request(url,payload=json_payload)


'''
