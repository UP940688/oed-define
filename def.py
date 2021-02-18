#!/usr/bin/env python3
"""
Gets a word definition (and optionally example) from Oxford English Dictionaries.
"""

import sys
import requests

# You'll need to supply these yourself.

API_INFO = {
    "app_id"  : "",
    "app_key" : ""
}

class Word:
    """Some wrappers to get the information from OED"""
    def __init__(self, word):
        self.base = "https://od-api.oxforddictionaries.com/api/v2/entries"
        self.lang = "en-gb" # change if applicable
        self.word = word
        self.filter = "fields=definitions,examples"
        self.url = f"{self.base}/{self.lang}/{self.word.lower()}?{self.filter}"
        self.result = None

    def get_data(self):
        """Retrieve data from OED API."""
        with requests.get(self.url, headers=API_INFO) as req:
            if req.status_code != 200:
                print(f"Error retrieving data from API: {req.status_code}", file=sys.stderr)
                sys.exit(1)
            # their json makes me wanna cry, but it's just accessing the 0th indexes.
            result = req.json()["results"][0]["lexicalEntries"][0]
            self.result = result["entries"][0]["senses"][0]

    def get_definition(self):
        """Return definition of self.word."""

        # in some cases, OED can return examples but
        # not definitions. 
        if "definitions" not in self.result.keys():
            return "Could not find definition"
        return self.result["definitions"][0]

    def get_example(self):
        """"Return an example for self.word."""
        try:
            return self.result["examples"][0]["text"]
        except:
            return None


def main():
    """Retrieve definition for word."""

    # Very stupid arg parsing, but we only expect max. 1 arg
    if len(sys.argv) == 2:
        word = sys.argv[1]
    elif len(sys.argv) == 3:
        word = sys.argv[2]
    else:
        print("Please pass up to one argument and one word.", file=sys.stderr)
        sys.exit(1)

    w = Word(word)
    w.get_data()
    defn = w.get_definition()
    print(f"{word} ~ {defn}")

    if "-e" in sys.argv or "--example" in sys.argv:
        if ex := w.get_example():
            print(f"ex. {ex}")

if __name__ == "__main__":
    main()
