import MySQLdb
import MySQLdb.cursors
import flask
import configparser
import os

def read_config_section(config_file_name: str,
                        section: str) -> dict:
    config = configparser.ConfigParser()
    config.read(config_file_name)
    return dict(config[section if section is not None else 'client'])


mysql_config = read_config_section(os.path.join(os.path.expanduser("~"),
                                                ".my.cnf"),
                                   'client')
print(mysql_config)
db_conn = MySQLdb.connect(*[mysql_config[k]
                            for k in ['host', 'user', 'password', 'database']])

webapp = flask.Flask(__name__, static_url_path='/static')

def wrapper(inputText):
    return f"<html> <body> {inputText} </body> </html>"

@webapp.route('/')
def displaylinks():
    return flask.send_from_directory('static','home.html')

@webapp.route('/display/artist')
def display_artist():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM Artist ORDER BY Name ASC')
    results = cursor.fetchall() 
    res_html = '<table border = "1">'
    for Name, Email, Genre, BirthDate, ArtistID, NumberOfAlbums in results:
        res_html += f'<tr><td> {Name} </td> <td> {Email} </td> <td> {Genre} </td> <td> {BirthDate} </td> <td> {ArtistID} </td> <td> {NumberOfAlbums} </td> </tr>'
    res_html += f'</table>'
    return wrapper(res_html)
    

@webapp.route('/display/album')
def display_album():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM Album ORDER BY ArtistName ASC')
    results = cursor.fetchall() 
    res_html = '<table border = "1">'
    for ArtistName, AlbumID, Genre, ReleaseDate, NumberOfSongs, DurationOfAlbum in results:
        res_html += f'<tr><td> {ArtistName} </td> <td> {AlbumID} </td> <td> {Genre} </td> <td> {ReleaseDate} </td> <td> {NumberOfSongs} </td> <td> {DurationOfAlbum} </td> </tr>'
    res_html += f'</table>'
    return wrapper(res_html)

@webapp.route('/display/song')
def display_song():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM Song ORDER BY ArtistName ASC')
    results = cursor.fetchall() 
    res_html = '<table border = "1">'
    for ArtistName, SongID, ReleaseDate, SongDuration, Genre, SongName in results:
        res_html += f'<tr><td> {ArtistName} </td> <td> {SongID} </td> <td> {ReleaseDate} </td> <td> {SongDuration} </td> <td> {Genre} </td> <td> {SongName} </td> </tr>'
    res_html += f'</table>'
    return wrapper(res_html)

@webapp.route('/create_artist', methods = ['POST'])
def add_artist():
    cursor = db_conn.cursor()
    args = flask.request.form.to_dict()
    columns = ['Name', 'Email', 'Genre', 'BirthDate', 'ArtistID', 'NumberOfAlbums']
    param_values = [args[c] for c in columns]
    columns_substr = ', '.join(columns)
    param_list = ['%s'] * len(columns)
    params_substr = ', '.join(param_list)
    query = f'INSERT INTO Artist ({columns_substr}) VALUES ({params_substr});'
    cursor.execute(query, param_values)
    db_conn.commit()
    return flask.send_from_directory('static', 'home.html')

@webapp.route('/create_album', methods = ['POST'])
def add_album():
    cursor = db_conn.cursor()
    args = flask.request.form.to_dict()
    columns = ['ArtistName', 'AlbumID', 'Genre', 'ReleaseDate', 'NumberOfSongs', 'DurationOfAlbum']
    param_values = [args[c] for c in columns]
    columns_substr = ', '.join(columns)
    param_list = ['%s'] * len(columns)
    params_substr = ', '.join(param_list)
    cursor.execute(f'INSERT INTO Album ({columns_substr}) VALUES ({params_substr});', param_values)
    db_conn.commit()
    return flask.send_from_directory('static', 'home.html')

@webapp.route('/create_song', methods = ['POST'])
def add_song():
    cursor = db_conn.cursor()
    args = flask.request.form.to_dict()
    columns = ['ArtistName', 'SongID', 'ReleaseDate', 'SongDuration', 'Genre', 'SongName']
    param_values = [args[c] for c in columns]
    columns_substr = ', '.join(columns)
    param_list = ['%s'] * len(columns)
    params_substr = ', '.join(param_list)
    cursor.execute(f'INSERT INTO Song ({columns_substr}) VALUES ({params_substr});', param_values)
    db_conn.commit()
    return flask.send_from_directory('static', 'home.html')

# ##get_tables = webapp.route('/')(get_tables)