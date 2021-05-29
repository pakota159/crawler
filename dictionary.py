import urllib.request
import json

def translate(word):
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/{}'.format(word)
    print(url)
    try:
        with urllib.request.urlopen(url) as res:
            data = json.loads(res.read())
            # print(json.dumps(data, indent=4, sort_keys=True))
            meaning = ""
            example = ""
            try:
                definition = data[0]["meanings"][0]["definitions"][0]
                if "definition" in definition:
                    meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
                if "example" in definition:
                    example = data[0]["meanings"][0]["definitions"][0]["example"]
                return (meaning, example)
            except:
                return (meaning, example)
    except:
        return ("", "")