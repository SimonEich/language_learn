import sqlite3
import os


class Database:
    def __init__(self) -> None:
        self.i = 0
        self.conn()
        self.create()
        self._remove_empty_entries()
        self._remove_duplicate()
        self.read_db()
        self.get_random_word()
        self.read_db()
        
    def delete_word(self, word: str) -> None:
        self.cursor.execute("DELETE FROM words WHERE word = ?", (word,))
        self.conn.commit()
        print(f"Deleted word: {word}")
        
    def _remove_empty_entries(self) -> None:
        # Delete rows where word or translation is empty or just whitespace
        self.cursor.execute("""
            DELETE FROM words
            WHERE TRIM(word) = '' OR TRIM(translation) = ''
        """)
        self.conn.commit()
        print("Empty entries removed from the database.")

        
    def conn(self) -> None:
        self.conn = sqlite3.connect('cards.db')
        self.cursor = self.conn.cursor()
        
    def create(self) -> None:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS words
                                (word TEXT PRIMARY KEY, translation TEXT, count INT)''')
        self.conn.commit()
    
    def insert(self) -> None:
        while self.i < len(self.data):
            word, translation = self.data[self.i][0], self.data[self.i][1]
            self.cursor.execute("INSERT OR IGNORE INTO words VALUES (?, ?, ?)", (word, translation, 0))
            self.i += 1
        self.conn.commit()
        
    def insert_word(self, word: str, translation: str) -> None:
        # Trim whitespace and check for empty fields
        if not word.strip() or not translation.strip():
            print("Both fields must be filled.")
            return

        # Check if the word already exists in the database
        self.cursor.execute("SELECT * FROM words WHERE word = ?", (word,))
        existing = self.cursor.fetchone()

        if existing:
            print("Word already exists.")
            return  # Exit early if duplicate

        # Insert the word into the database
        self.cursor.execute("INSERT INTO words VALUES (?, ?, ?)", (word, translation, 0))
        self.conn.commit()

        # Verify insertion
        self.cursor.execute("SELECT * FROM words WHERE word = ? AND translation = ?", (word, translation))
        result = self.cursor.fetchone()

        if result:
            print("Success")
        else:
            print("Failed to insert the word.")


    def update_word(self, old_word: str, new_word: str, new_translation: str) -> None:
        self.cursor.execute(
            "UPDATE words SET word = ?, translation = ? WHERE word = ?",
            (new_word, new_translation, old_word)
        )
        self.conn.commit()
        print(f"Updated '{old_word}' to '{new_word}': '{new_translation}'")

    
    def _remove_duplicate(self) -> None:
        # Delete duplicate Spanish words, keeping the one with the lowest rowid
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

        
    def read_db(self) -> None:
        self.cursor.execute("SELECT * FROM words")
        data_db = self.cursor.fetchall()
        return data_db
    
    def get_random_word(self) -> None:
        self.cursor.execute("SELECT * FROM words WHERE count = 0 ORDER BY RANDOM() LIMIT 1;")
        row = self.cursor.fetchone()
        return row
    
    def insert_bulk_words_from_text(self, text: str) -> None:
        lines = text.strip().splitlines()
        inserted = 0
        skipped = 0

        for line in lines:
            if ':' not in line:
                continue  # skip invalid lines

            word, translation = map(str.strip, line.split(':', 1))
            if not word or not translation:
                continue  # skip empty entries

            # Check if the word already exists
            self.cursor.execute("SELECT 1 FROM words WHERE word = ?", (word,))
            if self.cursor.fetchone():
                skipped += 1
                continue

            self.cursor.execute("INSERT INTO words VALUES (?, ?, ?)", (word, translation, 0))
            inserted += 1

        self.conn.commit()
        print(f"{inserted} new words inserted. {skipped} duplicates skipped.")


    def insert_from_file(self, file_path: str) -> None:
        
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
                continue  # Skip invalid lines
            
            word, translation = map(str.strip, line.split(':', 1))

            if not word or not translation:
                continue  # Skip if either part is empty
            
            # Check if the word already exists
            self.cursor.execute("SELECT 1 FROM words WHERE word = ?", (word,))
            if self.cursor.fetchone():
                skipped += 1
                continue
            
            self.cursor.execute("INSERT INTO words VALUES (?, ?, ?)", (word, translation, 0))
            inserted += 1

        self.conn.commit()
        print(f"Finished inserting from file: {inserted} new words added, {skipped} duplicates skipped.")
        
    def get_training_words(self):
        self.cursor.execute("""
            SELECT word, translation, count
            FROM words
            WHERE count = (SELECT MIN(count) FROM words)
            ORDER BY count ASC
            LIMIT 10;
        """)
        return self.cursor.fetchall()
    
    def increase_count(self, word):
        self.cursor.execute("""
                            UPDATE words
                            SET count = count + 1
                            WHERE word = ?
                            """, (word,))
        self.conn.commit()
        print(f"Updated count for '{word}'")

    def reset_count_db(self):
        self.cursor.execute("""
                            UPDATE words
                            SET count = 0
                            """)
        self.conn.commit()