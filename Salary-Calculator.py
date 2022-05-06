#Info: Simple CTC-Cost-To-Company Calculator in Base/Quote currencies USD/AED.
#Using Marketdata live API.
#Author: Haseeb Mir @HM.
#Date: 05/06/2022.

import requests
from num2words import num2words
import sys

#Variables for Server Api,Base Urls.
url = "https://marketdata.tradermade.com/api/v1/live"
api_key = "" #Enter API key here.
verbose = False

n2w_lang = 'en' #Num2Words language.
"""
* en (English, default)
* en_GB (English - Great Britain)
* en_IN (English - India)
* ar (Arabic)
* cz (Czech)
* de (German)
* dk (Danish)
Check Num2word Lang section : https://github.com/savoirfairelinux/num2words
"""


#Method to get Exchanges rate from API.    
def get_api_exchange_rate(from_currency:str, to_currency:str):
    exchange_rate:float = 0.0
    
    try:
        #Send query params.
        currency = from_currency + to_currency
        query = {"currency":currency,"api_key":api_key}
        
        #Send request to server API.
        response = requests.get(url, params=query)
        #Get the response in Quotes.
        result = response.json()
        if verbose:
            print(result)
        exchange_rate = result['quotes'][0]['mid']
    
    except Exception as e:
        print("Error while connecting to Forex API. " + str(e))
         
    return exchange_rate

#Method to calculate CTC.
def get_ctc_rate(salary:int,from_currency:str, to_currency:str,months:int=12):
    ctc_rate:float = 0
    if from_currency == to_currency: #No conversion for same currency.
        ctc_rate = salary * months
    else:
        exchange_rate = get_api_exchange_rate(from_currency,to_currency)
        if verbose:
            print("exchange_rate: ",exchange_rate)
            
        base_salary = salary * exchange_rate
        ctc_rate = base_salary * months
    return ctc_rate

#Method to get ctc in words.
def get_ctc_words(ctc:float,lang:str='en'):
    ctc_rate_word = num2words(ctc_rate,lang=lang)
    return ctc_rate_word

# Main method.
if __name__ == "__main__" :
    
    try:
        argc = len(sys.argv)
        if argc <= 1:
            raise Exception("\nUsage " + sys.argv[0] + " salary from_currency to_currency months\nSalary: 15000\nfrom_currency: 'AED'\nto_currency:'USD'\nmonths:12")
        if argc < 5:
            raise Exception("Application expected '5' parameters but only '" + str(argc) + "' were passed.")
        #Get the arguments from cmd.
        salary = int(sys.argv[1])
        from_curr = str(sys.argv[2])
        to_curr = str(sys.argv[3])
        months = int(sys.argv[4])
        
        #Run the CTC-Functions with provided arguments.
        ctc_rate = get_ctc_rate(salary,from_curr,to_curr,months)
        if ctc_rate > 0:
            ctc_rate_word = get_ctc_words(ctc_rate,n2w_lang)
            print("'" + str(ctc_rate) + "' : " + "'" + ctc_rate_word + "'")
    
    except Exception as e:
        print("Exception in main: " + str(e))
    