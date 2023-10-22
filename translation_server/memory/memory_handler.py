"""

Memory handler proxies the translation and compares the sentences to pre-translated sentences.

To use in RAM memory, make sure to configure :memory: as the database location
Otherwise all translations are stored, this is not ideal for privacy.

Version 1 uses SQLite to store sentences, storage is cheap.
Version 2 will perhaps use a Vector database


"""