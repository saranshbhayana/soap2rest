import xmltodict
import json
from django.http import HttpResponse
from rest_framework.decorators import api_view
import requests

@api_view(['POST'])
def convert_soap_to_rest(request):
    # Extract the SOAP envelope from the request data
    soap_envelope = request.body.decode('utf-8')

    # Convert the SOAP envelope to a Python dictionary using xmltodict
    soap_dict = xmltodict.parse(soap_envelope)

    # Extract the LoanQuotes element from the SOAP dictionary
    loan_quotes = soap_dict['soapenv:Envelope']['soapenv:Body']['LoanQuotes']

    # Check if there's only one LoanQuote or multiple LoanQuotes
    if isinstance(loan_quotes['LoanQuote'], list):
        # If multiple LoanQuotes, assign the list of LoanQuotes
        loan_quotes_list = loan_quotes['LoanQuote']
    else:
        # If only one LoanQuote, create a list with that single LoanQuote
        loan_quotes_list = [loan_quotes['LoanQuote']]

    # Initialize an empty list to store the LoanQuote data
    loan_quote_data = []

    # Loop through each LoanQuote and extract the relevant data dynamically
    for loan_quote in loan_quotes_list:
        loan_quote_info = {}
        for key, value in loan_quote.items():
            loan_quote_info[key] = value


        # Create a dictionary representing the LoanQuote data
        loan_quote_data.append(loan_quote_info)

    # Define the REST endpoint where the converted request will be sent
    rest_endpoint = 'https://soap2rest.free.beeceptor.com/soap2rest'  # Replace with your actual REST API endpoint

    # Make a REST POST call with the aggregated LoanQuote data
    headers = {'Content-Type': 'application/json'}
    response = requests.post(rest_endpoint, json=loan_quote_data, headers=headers)

    # Return the REST API response back to the client
    return HttpResponse(response.text, content_type='application/json')
