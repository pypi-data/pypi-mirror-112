import json
import os.path
import sys


class LanguageAccessorFactory:
    @staticmethod
    def create(db_file_name, item):
        with open(db_file_name, "r", encoding='UTF-8-sig') as file:
            json_object = json.load(file)
        for element in json_object:
            if element["english"] == item:
                return LanguageAccessor(element)
        raise Exception("No such english word found")


class LanguageAccessor:
    def __init__(self, json_object: json):
        self.json_object = json_object

    def get(self, language: str):
        return self.json_object[language]


class LanguageAdder:
    @staticmethod
    def add(filename, to_add: list):
        """
        Adding a word to the dictionary
        :param filename: The name of the db file
        :param to_add: List in format [("English", "English words or phrases
        or sentences"), ("OtherLanguage", "Words or phrases or sentences in the other language"), ...]. English should be
        the first index of the list. You should pass a list of tuples for this.
        """
        with open(filename, "r", encoding='UTF-8-sig') as file:
            language_db = json.load(file)
        added = False
        for database in language_db:
            if "english" in database:
                if database["english"] == [x[1] for x in to_add][0]:
                    to_add.pop(0)
                    added = True
                    for language, element in to_add:
                        database[language] = element
            else:
                raise Exception("No english field which is the standard for adding other languages")
        if not added:
            to_append = {}
            for language, element in to_add:
                to_append[language] = element
            language_db.append(to_append)
        with open(filename, "w", encoding='UTF-8-sig') as file_write:
            file_write.write(json.dumps(language_db, ensure_ascii=False))


database_file = "../database.json"
sys.argv.pop(0)
if sys.argv[0] == "--database" and len(sys.argv) >= 2 and os.path.isfile(sys.argv[1]):
    database_file = "../database.json"
    sys.argv.pop(0)
    sys.argv.pop(0)
elif sys.argv[0] == "--database" and len(sys.argv) >= 2 and not os.path.isfile(sys.argv[1]):
    print("The specified database file is not valid")
    exit(0)
parameter_arguments = []
if len(sys.argv) % 2 == 0:
    language_codes = []
    values = []
    pairs = []
    state = True
    captured = ""
    for arg in sys.argv:
        if arg.startswith("\""):
            state = False
        if arg.endswith("\"") and state is False:
            parameter_arguments.append(captured)
        if state:
            parameter_arguments.append(arg)
        else:
            captured += (" " + arg)
    for index, arg in list(enumerate(parameter_arguments, start=0)):
        if index % 2 == 0:
            language_codes.append(arg)
        else:
            values.append(arg)
    for index, code in list(enumerate(language_codes, start=0)):
        pairs.append((code, values[index]))
    LanguageAdder.add(database_file, pairs)
else:
    print("The number of languages and the values does not match")
    exit(0)
