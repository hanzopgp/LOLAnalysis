from urllib import response
import requests
import json
from decorator import request # custom decorator
from constant import (PUUIS_ENDPOINT, HEADERS, MATCHS_ENDPOINTS, MATCH_DETAIL_ENDPOINTS,DIVISION_ENDPOINT) # endpoints


class UserDataExtractor: 

    """
        A class responsible for extracting user related info. 
    """
    @request
    def get_puuid_by_account_id(self, account_id): 
        """
            retrieve a user's puuid
        """
        endpoint = PUUIS_ENDPOINT + account_id
        puuid = requests.get(endpoint, headers=HEADERS)["puuid"]
        return {
            "response" : puuid, 
            "endpoint" : endpoint
        }


    @request
    def retrieve_matches(self, puuid): 
        """
            Returns a list of game'id
        """
        endpoint = MATCHS_ENDPOINTS + f"{puuid}/ids?type=ranked&start=0&count=25"
        r = requests.get(endpoint, headers=HEADERS)
        return {
            "response" : r, 
            "endpoint" : endpoint
        }




class MatchDataExtractor: 
    """
        A class responsible for extracting a match informations
    """
    
    @request
    def retrieve_match_content(self, match_id): 
        """
            Returns a game's content by its id
        """
        endpoint = MATCH_DETAIL_ENDPOINTS + match_id
        r = requests.get(endpoint, headers=HEADERS)
        
        return {
            "response" : r, 
            "endpoint" : endpoint
        }

