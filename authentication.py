import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1

# https://requests-oauthlib.readthedocs.io/en/latest/oauth1_workflow.html
# https://pypi.org/project/requests-oauthlib/0.3.1/
# https://developer.trademe.co.nz/

# Please read the TradeMe's documentation on how to obtain the consumerkey and consumersecretkey before begin
# This is a OAuth1 authentication script to obtain OAuth token and OAuth token secret.
# Once this key is obtained, this script does not need to be execute anymore.
# Refer to TradeMe's API Documentation for more information

consumerkey = None
consumersecretkey = None

consumerkey = input("Please enter your Consumer Key: ")
consumersecretkey = input("Please enter your Consumer Secret Key: ")
print("Your Consumer Key is: "+ consumerkey)
print("Your Consumer Secret Key is: " + consumersecretkey)

temporarycredentials = []
permanenttoken = []

def get_temporary_token():
    #create an object of OAuth1Session    
    request_token = OAuth1Session(client_key=consumerkey,client_secret=consumersecretkey)

    # TradeMe endpoint to get request token
    url = 'https://secure.trademe.co.nz/Oauth/RequestToken?scope=MyTradeMeRead,MyTradeMeWrite'

    # get request_token_key, request_token_secret and other details
    data = request_token.get(url)
    print("\nRequesting Temporary token and token secret")
    print("Returned Data : " + data.text + '\n')
    
    # Split the string to get relevant data 
    data_token = str.split(data.text, '&')
    ro_key = str.split(data_token[0], '=')
    ro_secret = str.split(data_token[1], '=')

    # Assign split keys to variable
    temporary_key = ro_key[1]
    temporary_secret = ro_secret[1]
    print("Temporary Oauth Token: " + temporary_key)
    print("Temporary Oauth Secret Token: " + temporary_secret)

    temporary = [temporary_key, temporary_secret]
    return temporary

def getuseraccess():
    base_authorization_url = 'https://secure.trademe.co.nz/Oauth/Authorize'
    authorize_url = base_authorization_url + '?oauth_token='
    authorize_url = authorize_url + temporarycredentials[0]

    print ('\nPlease visit the link to authorize,', authorize_url)
    verifier = input('Please input the verifier displayed on the screen: ')
    print("Verifer Data = ",verifier)
    return verifier

def finaltoken():
    print("\nObtaining Permanent OAuth Token & OAuth Token Secret")
    access_token_url = ' https://secure.trademe.co.nz/Oauth/AccessToken'
    oauth = OAuth1Session(consumerkey,
                          client_secret=consumersecretkey,
                          resource_owner_key=temporarycredentials[0],
                          resource_owner_secret=temporarycredentials[1],
                          verifier=verifier)
                          
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    OAuth_key = oauth_tokens.get('oauth_token')
    OAuth_secret = oauth_tokens.get('oauth_token_secret')

    print('Permanent OAuth Token = ', OAuth_key)
    print('Permanent OAuth Token Secret = ', OAuth_secret)

    permanenttoken = [OAuth_key,OAuth_secret]
    return permanenttoken

def testapi():
    Oauth_Token =permanenttoken[0]
    Oauth_Token_Secret =permanenttoken[1]

    tradeMe_request = OAuth1Session(consumerkey,consumersecretkey,Oauth_Token,Oauth_Token_Secret)
    #Depending on what you want to search , input the url here
    usersummary = 'https://api.trademe.co.nz/v1/MyTradeMe/Summary.json?'

    # Get the search page
    returnedPageAll = tradeMe_request.get(usersummary)
    print("\nStatus Code: ",returnedPageAll)
    print("Returned Data: ",returnedPageAll.text)

if __name__ == "__main__":
    temporarycredentials = get_temporary_token()
    verifier = getuseraccess()
    permanenttoken = finaltoken()
    testapi()
