import json
import argparse
from db import TweetStore
from textblob import TextBlob

# json files
JSON_PATH = "json_files/"
FILE_DICT = {
    "db_auth": "db_auth.json",
}

def get_args():
    """ Obtaining args from terminal """
    parser = argparse.ArgumentParser(description="Add senpy to all docs in the db")

    parser.add_argument("-db", "--db_name", type = str, required = True, 
                        help = "Name of Database for storing")

    parser.add_argument("-na", "--num_process", type = int, required = True, 
                        help = "Number of processes adding senpy to this db")

    parser.add_argument("-id", "--id", type = int, required = True, 
                        help = "Current process id / number, should start from 0")

    args = parser.parse_args()
    
    return args

def read_jsons():
    """ Read required json data files """
    with open(JSON_PATH + FILE_DICT["db_auth"], "r") as f:
        db_auth = json.load(f)
    return db_auth

def main():

    # get arguments
    args = get_args()

    db_auth = read_jsons()
    
    # db url
    url = "http://" + db_auth["user"] + ":" + db_auth["pwd"] \
            + "@" + db_auth["ip"] + ":" + db_auth["port"] + "/"

    # initialise DB
    storage = TweetStore(args.db_name, url)

    db = storage.get_db()

    for doc_id in db:

        # more than one process working
        if (args.num_process > 1):
            if (int(doc_id) % args.num_process) != args.id:
                # not the job of this process
                continue
                
        doc = db[doc_id]
        if "textblob" not in doc.keys():
            doc["textblob"] = TextBlob(doc["text"]).sentiment
            db[doc_id] = doc
            print("UPDATE DOC ", doc["_id"])

if __name__ == "__main__":
    main()