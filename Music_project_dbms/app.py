from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# ✅ DATABASE CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootadmin@123",
    database="capstone"
)

cursor = conn.cursor(dictionary=True)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- SONGS ----------------
@app.route('/songs')
def songs():
    cursor.execute("""
    SELECT s.song_id, s.title, s.duration,
           a.name AS artist,
           g.genre_name,
           al.title AS album
    FROM songs s
    JOIN albums al ON s.album_id = al.album_id
    JOIN artists a ON al.artist_id = a.artist_id
    JOIN genres g ON s.genre_id = g.genre_id
    """)
    songs = cursor.fetchall()

    cursor.execute("SELECT * FROM albums")
    albums = cursor.fetchall()

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()

    return render_template("songs.html", songs=songs, albums=albums, genres=genres)


@app.route('/add_song', methods=['POST'])
def add_song():
    cursor.execute("""
    INSERT INTO songs (song_id, title, duration, album_id, genre_id)
    VALUES (%s, %s, %s, %s, %s)
    """, (
        request.form['song_id'],
        request.form['title'],
        request.form['duration'],
        request.form['album_id'],
        request.form['genre_id']
    ))
    conn.commit()
    return redirect('/songs')


@app.route('/delete_song/<int:id>')
def delete_song(id):
    # delete from child table first
    cursor.execute("DELETE FROM playlist_songs WHERE song_id=%s", (id,))
    cursor.execute("DELETE FROM songs WHERE song_id=%s", (id,))
    conn.commit()
    return redirect('/songs')

# ---------------- ARTISTS ----------------
@app.route('/artists')
def artists():
    cursor.execute("SELECT * FROM artists")
    data = cursor.fetchall()
    return render_template("artists.html", artists=data)


@app.route('/add_artist', methods=['POST'])
def add_artist():
    cursor.execute("INSERT INTO artists VALUES (%s, %s)",
                   (request.form['artist_id'], request.form['name']))
    conn.commit()
    return redirect('/artists')


@app.route('/delete_artist/<int:id>')
def delete_artist(id):
    # delete dependent albums -> songs -> playlist_songs if needed
    cursor.execute("""
    DELETE ps FROM playlist_songs ps
    JOIN songs s ON ps.song_id = s.song_id
    JOIN albums al ON s.album_id = al.album_id
    WHERE al.artist_id=%s
    """, (id,))

    cursor.execute("""
    DELETE s FROM songs s
    JOIN albums al ON s.album_id = al.album_id
    WHERE al.artist_id=%s
    """, (id,))

    cursor.execute("DELETE FROM albums WHERE artist_id=%s", (id,))
    cursor.execute("DELETE FROM artists WHERE artist_id=%s", (id,))
    conn.commit()
    return redirect('/artists')

# ---------------- ALBUMS ----------------
@app.route('/albums')
def albums():
    cursor.execute("""
    SELECT al.album_id, al.title, a.name
    FROM albums al
    JOIN artists a ON al.artist_id = a.artist_id
    """)
    albums = cursor.fetchall()

    cursor.execute("SELECT * FROM artists")
    artists = cursor.fetchall()

    return render_template("albums.html", albums=albums, artists=artists)


@app.route('/add_album', methods=['POST'])
def add_album():
    cursor.execute("INSERT INTO albums VALUES (%s, %s, %s)",
                   (request.form['album_id'],
                    request.form['title'],
                    request.form['artist_id']))
    conn.commit()
    return redirect('/albums')


@app.route('/delete_album/<int:id>')
def delete_album(id):
    cursor.execute("""
    DELETE FROM playlist_songs
    WHERE song_id IN (SELECT song_id FROM songs WHERE album_id=%s)
    """, (id,))

    cursor.execute("DELETE FROM songs WHERE album_id=%s", (id,))
    cursor.execute("DELETE FROM albums WHERE album_id=%s", (id,))
    conn.commit()
    return redirect('/albums')

# ---------------- PLAYLISTS ----------------
@app.route('/playlists')
def playlists():
    cursor.execute("SELECT * FROM playlists")
    playlists = cursor.fetchall()

    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()

    # ✅ SHOW playlist songs
    cursor.execute("""
    SELECT p.name AS playlist, s.title
    FROM playlist_songs ps
    JOIN playlists p ON ps.playlist_id = p.playlist_id
    JOIN songs s ON ps.song_id = s.song_id
    """)
    playlist_songs = cursor.fetchall()

    return render_template("playlists.html",
                           playlists=playlists,
                           songs=songs,
                           playlist_songs=playlist_songs)


@app.route('/add_playlist', methods=['POST'])
def add_playlist():
    cursor.execute("""
    INSERT INTO playlists (playlist_id, name)
    VALUES (%s, %s)
    """, (request.form['playlist_id'], request.form['name']))
    conn.commit()
    return redirect('/playlists')


@app.route('/delete_playlist/<int:id>')
def delete_playlist(id):
    # ✅ FIX FK ISSUE
    cursor.execute("DELETE FROM playlist_songs WHERE playlist_id=%s", (id,))
    cursor.execute("DELETE FROM playlists WHERE playlist_id=%s", (id,))
    conn.commit()
    return redirect('/playlists')


@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    cursor.execute("""
    INSERT INTO playlist_songs (playlist_id, song_id)
    VALUES (%s, %s)
    """, (request.form['playlist_id'], request.form['song_id']))
    conn.commit()
    return redirect('/playlists')

# ---------------- SEARCH ----------------
@app.route('/search')
def search():
    query = request.args.get('query')

    cursor.execute("""
    SELECT s.song_id, s.title, s.duration,
           a.name AS artist,
           g.genre_name,
           al.title AS album
    FROM songs s
    JOIN albums al ON s.album_id = al.album_id
    JOIN artists a ON al.artist_id = a.artist_id
    JOIN genres g ON s.genre_id = g.genre_id
    WHERE s.title LIKE %s OR a.name LIKE %s
    """, (f"%{query}%", f"%{query}%"))

    songs = cursor.fetchall()

    cursor.execute("SELECT * FROM albums")
    albums = cursor.fetchall()

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()

    return render_template("songs.html", songs=songs, albums=albums, genres=genres)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)