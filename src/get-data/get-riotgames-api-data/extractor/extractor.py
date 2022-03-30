from urllib import response
import requests
import json
from decorator import request
from soupsieve import match # custom decorator
from constant import (
    PUUID_ENDPOINT, 
    MATCH_ENDPOINT, 
    MATCH_DETAIL_ENDPOINTS, 
    MATCH_DETAIL_TIMELINE, 
    HEADERS, 
    RIOT_SERVER, 
    REGION_ENDPOINT
    ) # endpoints


def get_server(server):

    if server.lower() not in RIOT_SERVER: 
        raise ValueError(f"{server} is unkown. Please, select one of the following servers : ", RIOT_SERVER.keys())
    return RIOT_SERVER[server.lower()]


def get_region(region): 
    if region.lower() not in REGION_ENDPOINT: 
        raise ValueError(f"{region} is unkown. Please, select one of the following regions : ", REGION_ENDPOINT.keys())
    return REGION_ENDPOINT[region.lower()]


class UserDataExtractor: 

    """
        A class responsible for extracting user related info. 
    """
    @request
    def get_user_info(self, account_id, server="EUW1"): 
        """
            retrieve user informations and the endpoint in order to be consumed
        """
        server = get_server(server)
        endpoint = server + PUUID_ENDPOINT + account_id
        puuid = requests.get(endpoint, headers=HEADERS)
        print(puuid)
        return {
            "response" : puuid, 
            "endpoint" : endpoint
        }


    @request
    def get_matches(self, puuid, region="europe"): 
        """
            Returns a list of game'id and the endpoint in order to be consumed
        """
        region = get_region(region)
        endpoint = region + MATCH_ENDPOINT + f"{puuid}/ids?type=ranked&start=0&count=25"
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
    def retrieve_match_content(self, match_id, region="europe"): 
        """
            Returns a game's content and the endpoint in order to be consumed
        """
        region = get_region(region)
        endpoint = region + MATCH_DETAIL_ENDPOINTS + match_id
        r = requests.get(endpoint, headers=HEADERS)

        return {
            "response" : r, 
            "endpoint" : endpoint
        }



# extractor = UserDataExtractor() 
# d_puuid = extractor.get_user_info("eK-5G4INu5yvmAbQmxHkS3gSdan6EUCzfZ9dS0EbJCmlawM")
# puuid = d_puuid["puuid"]
# matches = extractor.get_matches(puuid)
# print(matches)

# match_extractor = MatchDataExtractor()
# content = match_extractor.retrieve_match_content(matches[0])
# print(content)