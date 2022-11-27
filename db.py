import sqlite3


def connect_to_db():
    con = sqlite3.connect("weather_db.db", check_same_thread=False)
    cur = con.cursor()
    create_tables(con, cur)
    return con, cur


def create_tables(con, cur):
    weather_table = """
    CREATE TABLE IF NOT EXISTS weather (
        id INT NOT NULL PRIMARY KEY,
        date VARCHAR(50) NOT NULL,
        temperature INT NOT NULL,
        description VARCHAR(25) NOT NULL,
        feels_like INT NOT NULL,
        pressure INT NOT NULL,
        humidity INT NOT NULL        
    );
    """
    forecast_table = """
       CREATE TABLE IF NOT EXISTS forecast (
           date VARCHAR(50) NOT NULL PRIMARY KEY,
           temperature INT NOT NULL
       );
       """
    cur.execute(weather_table)
    cur.execute(forecast_table)
    con.commit()
