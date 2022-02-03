
# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays 
                             (songplay_id serial, 
                             start_time timestamp NOT NULL,
                             user_id int NOT NULL , 
                             level varchar NOT NULL, 
                             song_id varchar, 
                             artist_id varchar, 
                             session_id int NOT NULL, 
                             location varchar NOT NULL , 
                             user_agent varchar NOT NULL,
                             PRIMARY KEY (songplay_id));""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users 
                        (user_id int, 
                        first_name varchar NOT NULL, 
                        last_name varchar NOT NULL,
                        gender varchar NOT NULL, 
                        level varchar NOT NULL,
                        PRIMARY KEY (user_id));
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs 
                        (song_id VARCHAR(18), 
                        title varchar NOT NULL, 
                        artist_id varchar NOT NULL, 
                        year int NOT NULL,                         
                        duration float NOT NULL,
                        PRIMARY KEY (song_id));
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists 
                          (artist_id varchar, 
                          name varchar NOT NULL, 
                          location varchar,                                
                          latitude float, 
                          longitude float,
                          PRIMARY KEY (artist_id));
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time 
                        (start_time timestamp PRIMARY KEY, 
                        hour int NOT NULL, 
                        day int NOT NULL, 
                        week int NOT NULL,                              
                        month int NOT NULL, 
                        year int NOT NULL, 
                        weekday int NOT NULL);
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays 
                            (
                            start_time, 
                            user_id, 
                            level, 
                            song_id, 
                            artist_id,                                      
                            session_id, 
                            location, 
                            user_agent) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING
                    
""")

user_table_insert = ("""INSERT INTO users 
                        (user_id, 
                        first_name, 
                        last_name, 
                        gender, 
                        level) 
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE 
                        SET level = excluded.level
""")

song_table_insert = ("""INSERT INTO songs 
                        (song_id, 
                        title, 
                        artist_id, 
                        year, 
                        duration) 
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""INSERT INTO artists 
                          (artist_id, 
                          name, 
                          location, 
                          latitude, 
                          longitude) 
                          VALUES (%s, %s, %s, %s, %s)
                          ON CONFLICT (artist_id) DO NOTHING
""")


time_table_insert = ("""INSERT INTO time 
                        (start_time, 
                        hour, 
                        day, 
                        week, 
                        month, 
                        year, 
                        weekday) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
""")

# FIND SONGS Implement the song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, and duration of a song. This one is a little more complicated since information from the songs table, artists table, and original log file are all needed for the songplays table. Since the log file does not specify an ID for either the song or the artist, you'll need to get the song ID and artist ID by querying the songs and artists tables to find matches based on song title, artist name, and song duration time.

song_select = ("""SELECT songs.song_id, artists.artist_id 
                  FROM songs join artists ON artists.artist_id = songs.artist_id 
                  WHERE songs.title = %s and artists.name = %s and songs.duration = %s
                  
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]