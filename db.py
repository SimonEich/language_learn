"""
Database management module for a simple word-translation flashcard system.

This module defines a `Database` class that manages a SQLite database of words and their translations.
It provides functionality to insert, delete, update, and query word pairs, including bulk inserts from text or files,
removing duplicates, selecting words for training, and managing usage counts.
"""

import sqlite3
import os


class Database:
    """
    A class to manage a SQLite database of word-translation pairs for language learning flashcards.
    """

    def __init__(self) -> None:
        """
        Initialize the database, establish connection, create tables, and clean up existing data.
        """
        self.i = 0
        self.conn()
        self.create()
        self._remove_empty_entries()
        self._remove_duplicate()
        self.read_db()
        self.get_random_word()
        self.read_db()
        
    def conn(self) -> None:
        """
        Establish a connection to the SQLite database and create a cursor.
        """
        self.conn = sqlite3.connect('cards.db')
        self.cursor = self.conn.cursor()
        
    def create(self) -> None:
        """
        Create the 'words' table if it does not already exist.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS words
                                (word TEXT PRIMARY KEY, translation TEXT, count INT)''')
        self.conn.commit()
    
    def delete_word(self, word: str) -> None:
        """
        Delete a word from the database.

        Args:
            word (str): The word to delete.
        """
        self.cursor.execute("DELETE FROM words WHERE word = ?", (word,))
        self.conn.commit()
        print(f"Deleted word: {word}")
        
    def _remove_empty_entries(self) -> None:
        """
        Remove entries with empty or whitespace-only words or translations.
        """
        self.cursor.execute("""
            DELETE FROM words
            WHERE TRIM(word) = '' OR TRIM(translation) = ''
        """)
        self.conn.commit()
        print("Empty entries removed from the database.")

    def _remove_duplicate(self) -> None:
        """
        Remove duplicate words, keeping only the first occurrence based on rowid.
        """
        self.cursor.execute("""
            DELETE FROM words
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM words
                GROUP BY TRIM(word)
            )
        """)
        self.conn.commit()
        print("Duplicate Spanish words removed.")

    def insert(self) -> None:
        """
        Insert words from self.data list into the database.
        """
        while self.i < len(self.data):
            word, translation = self.data[self.i][0], self.data[self.i][1]
            self.cursor.execute("INSERT OR IGNORE INTO words VALUES (?, ?, ?)", (word, translation, 0))
            self.i += 1
        self.conn.commit()
        
    def insert_word(self, word: str, translation: str) -> None:
        """
        Insert a single word-translation pair into the database after validating input.

        Args:
            word (str): The word in the source language.
            translation (str): The translation of the word.
        """
        if not word.strip() or not translation.strip():
            print("Both fields must be filled.")
            return

        self.cursor.execute("SELECT * FROM words WHERE word = ?", (word,))
        existing = self.cursor.fetchone()

        if existing:
            print("Word already exists.")
            return

        self.cursor.execute("INSERT INTO words VALUES (?, ?, ?)", (word, translation, 0))
        self.conn.commit()

        self.cursor.execute("SELECT * FROM words WHERE word = ? AND translation = ?", (word, translation))
        result = self.cursor.fetchone()

        if result:
            print("Success")
        else:
            print("Failed to insert the word.")

    def update_word(self, old_word: str, new_word: str, new_translation: str) -> None:
        """
        Update an existing word and its translation.

        Args:
            old_word (str): The word to be updated.
            new_word (str): The new word.
            new_translation (str): The new translation.
        """
        self.cursor.execute(
            "UPDATE words SET word = ?, translation = ? WHERE word = ?",
            (new_word, new_translation, old_word)
        )
        self.conn.commit()
        print(f"Updated '{old_word}' to '{new_word}': '{new_translation}'")

    def read_db(self) -> list:
        """
        Read all entries from the database.

        Returns:
            list: All rows from the 'words' table.
        """
        self.cursor.execute("SELECT * FROM words")
        data_db = self.cursor.fetchall()
        return data_db

    def get_random_word(self) -> tuple:
        """
        Get a random word that has not been trained (count == 0).

        Returns:
            tuple: A word-translation pair from the database.
        """
        self.cursor.execute("SELECT * FROM words WHERE count = 0 ORDER BY RANDOM() LIMIT 1;")
        row = self.cursor.fetchone()
        return row

    def insert_bulk_words_from_text(self, text: str) -> None:
        """
        Insert multiple word-translation pairs from a given text input.

        Args:
            text (str): Multiline string with 'word:translation' pairs.
        """
        lines = text.strip().splitlines()
        inserted = 0
        skipped = 0

        for line in lines:
            if ':' not in line:
                continue

            word, translation = map(str.strip, line.split(':', 1))
            if not word or not translation:
                continue

            self.cursor.execute("SELECT 1 FROM words WHERE word = ?", (word,))
            if self.cursor.fetchone():
                skipped += 1
                continue

            self.cursor.execute("INSERT INTO words VALUES (?, ?, ?)", (word, translation, 0))
            inserted += 1

        self.conn.commit()
        print(f"{inserted} new words inserted. {skipped} duplicates skipped.")

    def insert_from_file(self, file_path: str) -> None:
        """
        Insert word-translation pairs from a file.

        Args:
            file_path (str): Path to a text file containing 'word:translation' lines.
        """
        if not os.path.exists(file_path):
            print(f"File '{file_path}' does not exist.")
            return

        inserted = 0
        skipped = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if ':' not in line or not line:
                continue
            
            word, translation = map(str.strip, line.split(':', 1))
            if not word or not translation:
                continue

            self.cursor.execute("SELECT 1 FROM words WHERE word = ?", (word,))
            if self.cursor.fetchone():
                skipped += 1
                continue
            
            self.cursor.execute("INSERT INTO words VALUES (?, ?, ?)", (word, translation, 0))
            inserted += 1

        self.conn.commit()
        print(f"Finished inserting from file: {inserted} new words added, {skipped} duplicates skipped.")

    def get_training_words(self) -> list:
        """
        Retrieve the 10 least-practiced word-translation pairs for training.

        Returns:
            list: List of 10 words with the lowest count values.
        """
        self.cursor.execute("""
            SELECT word, translation, count
            FROM words
            WHERE count = (SELECT MIN(count) FROM words)
            ORDER BY count ASC
            LIMIT 10;
        """)
        return self.cursor.fetchall()

    def increase_count(self, word: str) -> None:
        """
        Increment the usage count of a given word.

        Args:
            word (str): The word whose count will be increased.
        """
        self.cursor.execute("""
                            UPDATE words
                            SET count = count + 1
                            WHERE word = ?
                            """, (word,))
        self.conn.commit()
        print(f"Updated count for '{word}'")

    def reset_count_db(self) -> None:
        """
        Reset the training count for all words to zero.
        """
        self.cursor.execute("""
                            UPDATE words
                            SET count = 0
                            """)
        self.conn.commit()
