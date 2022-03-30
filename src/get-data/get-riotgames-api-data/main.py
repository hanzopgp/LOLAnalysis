from extractor import UserDataExtractor, MatchDataExtractor
from dataparser import PlayerParser, MatchParser  
from config import *


def main():

    user_extract = UserDataExtractor()
    match_extractor = MatchDataExtractor() 
    player_parser = PlayerParser(filename=PLAYER_CSV_PATH)
    match_parser = MatchParser(filename=MATCH_CSV_PATH)

    # d_puuid = user_extract.get_user_info("eK-5G4INu5yvmAbQmxHkS3gSdan6EUCzfZ9dS0EbJCmlawM")
    # puuid = d_puuid["puuid"]
    # matches = user_extract.get_matches(puuid)
    # content = match_extractor.retrieve_match_content(matches[0])

    # d_content = player_parser.preprocess_content(content, puuid)
    # print(d_content)
    # player_parser.write_into(d_content.keys())



if __name__ == "__main__": 
    main()