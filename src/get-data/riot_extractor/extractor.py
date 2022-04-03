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
    SUMM_ENDPOINT
    ) # endpoints


def get_server(server):
    """
        return server, region 
    """
    server += "1"
    if server.lower() not in RIOT_SERVER: 
        raise ValueError(f"{server} is unkown. Please, select one of the following servers : ", RIOT_SERVER.keys())
    return RIOT_SERVER[server.lower()]



class UserDataExtractor: 

    """
        A class responsible for extracting user related info. 
    """
    @request 
    def get_summoner_info(self, summoner_name, server="EUW1"): 
        """
            retrieve user informations based on its summoner's name, and the endpoint 
        """
        server, _ = get_server(server)
        endpoint = server + SUMM_ENDPOINT + summoner_name
        r = requests.get(endpoint, headers=HEADERS)
        return {
            "response" : r, 
            "endpoint" : endpoint
        }


    @request
    def get_user_info(self, account_id, server="EUW1"): 
        """
            retrieve user informations and the endpoint in order to be consumed
        """
        server, _ = get_server(server)
        endpoint = server + PUUID_ENDPOINT + account_id
        r = requests.get(endpoint, headers=HEADERS)
        return {
            "response" : r, 
            "endpoint" : endpoint
        }


    @request
    def get_matches(self, puuid, region="europe"): 
        """
            Returns a list of game'id and the endpoint in order to be consumed
        """
        _, region = get_server(region)
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
        _, region = get_server(region)
        endpoint = region + MATCH_DETAIL_ENDPOINTS + match_id
        r = requests.get(endpoint, headers=HEADERS)

        return {
            "response" : r, 
            "endpoint" : endpoint
        }

