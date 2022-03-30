"""
    URLS
"""


# PUUID_ENDPOINT : information regarding the user's account
PUUID_ENDPOINT = "/lol/summoner/v4/summoners/by-account/"#{encryptedAccountId}
# MATCH_ENDPOINT : list of match ids
MATCH_ENDPOINT = "/lol/match/v5/matches/by-puuid/" #{puuid}/idsGet
# MATCH_DETAIL_ENDPOINTS : a game's details
MATCH_DETAIL_ENDPOINTS = "/lol/match/v5/matches/" #{matchId}
# MACH_DETAIL_TIMELINE : a game's timeline info 
MATCH_DETAIL_TIMELINE = "/lol/match/v5/matches/" #{matchId}/timelineGet

