# Capstone-DBMS-Music-Library-Management-System

# 🎵 Music Library Management System

## 📌 Project Overview

The **Music Library Management System** is a web-based application developed to manage and organize music-related data such as songs, artists, albums, genres, and playlists.
It provides a user-friendly interface along with a structured relational database to efficiently perform operations like storing, retrieving, and analyzing music information.

---

## 🎯 Objectives

* Design a relational database schema for a music library
* Manage songs, artists, albums, genres, and playlists
* Implement full CRUD (Create, Read, Update, Delete) operations
* Execute SQL queries for searching and analyzing music data
* Develop a web interface connected to MySQL database

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS (Spotify-style UI)
* **Backend:** Python (Flask)
* **Database:** MySQL
* **Tools Used:** VS Code, MySQL CLI

---

## 🗂️ Database Schema

### Entities:

* Artists
* Albums
* Songs
* Genres
* Playlists
* Playlist_Songs (Junction Table)

### Relationships:

* Artist → Album (1:M)
* Album → Song (1:M)
* Genre → Song (1:M)
* Playlist ↔ Song (M:N)

---

## ⚙️ Features

### 🔹 CRUD Operations

* Add, view, and delete songs
* Add, view, and delete artists
* Add, view, and delete albums
* Create and delete playlists

### 🔹 Playlist Management

* Add songs to playlists
* View songs inside playlists
* Many-to-many relationship implementation

### 🔹 Search Functionality

* Search songs by title or artist

### 🔹 UI Features

* Dark theme (Spotify-inspired UI)
* Sidebar navigation
* Responsive tables and forms

---

## 🧪 Sample Functionalities

* Display all songs with artist, album, and genre
* Count number of songs per artist
* Filter songs based on duration
* Manage playlists dynamically

---

## 🚀 How to Run the Project

1. Clone or download the project
2. Install required libraries:

   ```bash
   pip install flask mysql-connector-python
   ```
3. Start MySQL and ensure database name is **capstone**
4. Update database credentials in `app.py` if needed
5. Run the Flask app:

   ```bash
   python app.py
   ```
6. Open browser and go to:

   ```
   http://127.0.0.1:5000/
   ```

---

## 📂 Project Structure

```
Music_project_dbms/
│
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── songs.html
│   ├── artists.html
│   ├── albums.html
│   └── playlists.html
│
├── static/
│   └── style.css
```

---

## 🔒 Constraints Used

* Primary Keys
* Foreign Keys
* NOT NULL constraints
* Referential Integrity

---

## 🎓 Academic Details

* **Name:** Sneha Gupta
* **Roll Number:** 2401010020
* **Submitted To:** Ms. Mansi Kajal

---

## 📌 Conclusion

This project demonstrates the practical implementation of database concepts such as normalization, relationships, and constraints using MySQL.
The integration with a web-based interface enhances usability and showcases real-world application of DBMS concepts.

---

## 🚀 Future Enhancements

* User authentication system
* Music recommendation system
* Audio playback feature
* Advanced analytics dashboard

---

✨ *This project reflects the integration of database design with modern web development practices.*
