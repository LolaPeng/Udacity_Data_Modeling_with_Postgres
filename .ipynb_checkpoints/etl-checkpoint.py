import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *




def process_song_file(cur, filepath):
    """
    process_song_file function processes a song file whose filepath has been provided as an arugment.
    It extracts the song data and artist data needed in future analysis to store them into the songs table and artist table.
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].drop_duplicates()
    artist_data = artist_data.values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

    

def process_log_file(cur, filepath):
    """
    process_log_file function processes a log file whose filepath has been provided as an arguement.
    It extracts usefull information from log file and store those data into time_table, user_table and songplay_table seperately     for further analysis.
    """
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']
    

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'])
    
    # insert time data records
    time_data = ([a, a.hour, a.day, a.weekofyear, a.month, a.year, a.dayofweek] for a in t)
    time_df = pd.DataFrame(time_data, columns = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday'])

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    process_data function put all data and file together based on the rules we built and process data for future analysis.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()