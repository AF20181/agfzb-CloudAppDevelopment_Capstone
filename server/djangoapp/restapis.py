import requests
import json
import ibm_watson
# import related models here
from requests.auth import HTTPBasicAuth
from . import models
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, state=None, dealerId=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if "api_key" in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            print(params)
            response = requests.get(
                url,
                params=params,
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', kwargs["api_key"])
                )
        else:
            response = requests.get(
                url,
                params=kwargs,
                headers={'Content-Type': 'application/json'}
                )
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        print("Network exception occurred")
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        json_data = json.loads(response.text)
        return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, state=None):
    results = []
    json_result = get_request(url, state, id)
    if json_result:
        if state:
            dealers = json_result["body"]["docs"]
            for dealer in dealers:
                dealer_obj = models.CarDealer(
                    address=dealer["address"],
                    city=dealer["city"],
                    full_name=dealer["full_name"],
                    id=dealer["id"],
                    lat=dealer["lat"],
                    lng=dealer["long"],
                    short_name=dealer["short_name"],
                    st=dealer["st"],
                    state=dealer["state"],
                    zip=dealer["zip"]
                )
                results.append(dealer_obj)
        #elif id:
        #        dealers = json_result["rows"]
        #        for dealer in dealers:
        #            dealer_obj = models.CarDealer(
        #            id=dealer["id"],
        #            )
        #        results.append(dealer_obj)
        else:
            dealers = json_result["body"]["rows"]
            for dealer in dealers:
                dealer_doc = dealer["doc"]
                dealer_obj = models.CarDealer(
                    address=dealer_doc["address"],
                    city=dealer_doc["city"],
                    full_name=dealer_doc["full_name"],
                    id=dealer_doc["id"],
                    lat=dealer_doc["lat"],
                    lng=dealer_doc["long"],
                    short_name=dealer_doc["short_name"],
                    st=dealer_doc["st"],
                    state=dealer_doc["state"],
                    zip=dealer_doc["zip"]
                )
                results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_by_id_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId)
    if json_result:
        reviews = json_result["body"]["docs"]
        for review in reviews:
            try:
                #review_doc = review["docs"]
                review_obj = models.DealerReview(
                    name = review["name"],
                    dealership = review["dealership"],
                    review = review["review"],
                    purchase = review["purchase"],
                    purchase_date = review["purchase_date"],
                    car_make = review['car_make'],
                    car_model = review['car_model'],
                    car_year = review['car_year'],
                    sentiment = analyze_review_sentiments(review["review"])
                )
            except:
                #review_doc = review["docs"]
                review_obj = models.DealerReview(
                    name = review["name"],
                    dealership = review["dealership"],
                    review = review["review"],
                    purchase=review["purchase"],
                    purchase_date = 'none',
                    car_make = 'none',
                    car_model = 'none',
                    car_year= 'none',
                    sentiment= analyze_review_sentiments(review["review"])
                )
            print(review_obj.review)
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/595df1f5-616d-496c-bcb2-b5652924010e"
    api_key = "1pKc6D2qbqQuO5RSwKTqVcE8ImXl-boKyxeogX30K9vt"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)
