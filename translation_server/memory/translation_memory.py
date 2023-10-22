

import SearchDb


class TranslationMemory:
    """
    Stores sentences, if they have been translated before, return translation

    If you want to translate from nl to en Translation memory will create a table called "nl_en"
    The table will contain input_text, output_text, translation_model (as an int), translation_counter (int of hits)

    models are hardcoded right now as:
        opus-mt = 0
        nllb = 1
        m2m100 = 2
    """

    def __init__(self, database_path: str):
        self.file_path = database_path
        self.database = SearchDb.SearchDb(self.file_path, thread_unsafe=True)  # async means it has to be thread unsafe
        self.model_map = {"opus-mt": 0,
                        "nllb": 1,
                        "m2m100": 2}


    def clean_memory(self):
        """
        Removes all translated sentences that only has 1 as translation_counter (Sentences that has never been seen twice)
        """
        pass

    def sentence_in_memory(self, input_language, output_language, input_text, model) -> str | None:
        """
        Check whether sentence has been translated before
        if so: return stored data as dict
        if not: return empty dict
        """
        language_combination_string = input_language + "_" + output_language  # Create table name
        self.database.multi_table_in_use = language_combination_string  # Set which table to use

        if language_combination_string not in self.database.tables:
            """ 
            If table does not exist, create it
            Unique values are input text, translated text and which model was used 
                The counter is only an iterator of how many hits the sentence has had
            """
            creation_header = [("input_text", "TEXT"), ("translated_text", "TEXT"), ("translation_model", "INTEGER"), ("translation_counter", "INTEGER")]
            unique_header = ["input_text", "translated_text", "translation_model"]  # Translation count should not be part of the unique combination
            self.database.multi_create_database(creation_header, custom_unique_header=unique_header)

        memory_dict = {"translated_text": None,
                       "translation_counter": 0}

        " First query the database "
        model_nr = self.model_map[model]
        search_tuple = [("input_text", input_text), ("translation_model", model_nr)]  # SearchDb requires tuples for multi key searches
        items = list(self.database.multi_search(search_tuple, return_dict=True))

        if len(items) > 0: # If there was a hit, return it
            for item in items:
                translated_text = item["translated_text"]
                translation_counter = item["translation_counter"]

                # Update the counter
                self.add_sentence_to_memory(input_language,
                                            output_language,
                                            input_text,
                                            translated_text,
                                            model,
                                            translation_counter + 1)

                memory_dict["translated_text"] = translated_text
                memory_dict["translation_counter"] = translation_counter

        return memory_dict  # Return the stored translated text



    def add_sentence_to_memory(self, input_language, output_language, input_text, translated_text, model, counter=1):

        language_combination_string = input_language + "_" + output_language  # Create table name
        model_nr = self.model_map[model]
        assert isinstance(model_nr, int)

        self.database.multi_table_in_use = language_combination_string  # Set which table to use
        self.database.multi_add((input_text, translated_text, self.model_map[model], counter)) # Add input text and translated text
        self.database.connection.commit()


