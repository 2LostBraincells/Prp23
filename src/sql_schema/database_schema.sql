CREATE TABLE IF NOT EXISTS person (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    personal_id TEXT,
    email TEXT,
    phone_number TEXT,
    birthday DATE,
    address Text,
    zip_code INT,
    city TEXT
);
CREATE TABLE IF NOT EXISTS class (
    name TEXT NOT NULL PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS program (
    name TEXT NOT NULL PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS elev (
    class INTEGER NOT NULL,
    program TEXT NOT NULL,
    person TEXT NOT NULL,

    FOREIGN KEY (person) REFERENCES person(id) ON DELETE CASCADE,
    FOREIGN KEY (class) REFERENCES class(name) ON DELETE CASCADE,
    FOREIGN KEY (person) REFERENCES program(name) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS elevkurser (
    elev INTEGER NOT NULL,
    kurs TEXT NOT NULL,

    FOREIGN KEY (elev) REFERENCES elev(id) ON DELETE CASCADE,
    FOREIGN KEY (kurs) REFERENCES kurs(id) ON DELETE CASCADE
);
