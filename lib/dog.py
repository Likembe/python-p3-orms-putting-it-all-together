import sqlite3

CONN = sqlite3.connect("dogs.db")
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        CURSOR.execute("CREATE TABLE IF NOT EXISTS dogs (id INTEGER PRIMARY KEY, name TEXT, breed TEXT)")
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?", (self.name, self.breed, self.id))
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog

    @classmethod
    def new_from_db(cls, row):
        if row:
            id, name, breed = row
            return cls(name, breed, id)
        return None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()
        return [cls(name, breed, id) for id, name, breed in rows]

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        if row:
            id, name, breed = row
            return cls(name, breed, id)
        return None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        if row:
            id, name, breed = row
            return cls(name, breed, id)
        return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog

    def update(self):
        CURSOR.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?", (self.name, self.breed, self.id))
        CONN.commit()

