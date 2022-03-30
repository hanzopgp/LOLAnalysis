from abc import abstractclassmethod, abstractmethod
import csv
from abc import ABC, abstractmethod


class CsvWritterMixin(ABC): 

    @abstractmethod
    def preprocess_content(self, content): 
        pass



class BaseCsvWritter: 

    def __init__(self, filename): 
        self.filename = filename

    
    def get_columns(self): 
        with open(self.filename) as csvfile: 
            file = csv.reader(csvfile, delimiter=",") 
            for row in file: 
                return ", ".join(row)


    def write_into(self, row): 
        """
            add a column of the preprocessed row into filename 
            note : row is a list
        """
        with open(self.filename, 'a+', newline='') as csvfile:
            current_file = csv.writer(csvfile, delimiter=",") 
            current_file.writerow(row)

        print("successfully wrote to ", self.filename)

        

    def flatten_and_write(self, row): 
        """
            convert the values of the dictionary to a single row and add it to the corresponding csv
        """
        return self.write_into(row.values())
        
        



class PlayerParser(CsvWritterMixin, BaseCsvWritter): 
     
    def __init__(self, filename):
        super(PlayerParser, self).__init__(filename)

    def preprocess_content(self, match_content, user_puuid):
        """
            Return the user match info by its puuid, as a dictionnary 
            Argument: 
                content : a match payload, 
                user_puuid
            out: 
                d : a dictionnary containing all infos
                None
        """

        data = {}
        info = match_content["info"]
        
        # collect info
        for k,v in info.items(): 
            if k != "participants": 
                data[k] = v

        participants = info["participants"]
        # collect player
        for participant in participants: 
            if participant["puuid"] == user_puuid: 
                # extract 
                for key in participant: 
                    if key == "challenges":
                        for k,v in participant["challenges"].items(): 
                            data[k] = v
                    if key != "perks":
                        data[key] = participant[key]
                return data
        return None



class MatchParser(CsvWritterMixin, BaseCsvWritter): 
    def __init__(self, filename):
        super(MatchParser, self).__init__(filename)


    def preprocess_content(self, match_content):
        """
            extract relevant match data 
        """
        data = {}
        meta = match_content["metadata"]
        info = match_content["info"]
        data["matchId"] = meta["matchId"]  
        data["game_id"] = info["gameId"]
        data["season"] = info["gameVersion"]
        data["gameDuration"] = info["gameDuration"]
        data["gameMode"] = info["gameMode"]
        data["gameCreation"] = info["gameCreation"] 

        return data        
