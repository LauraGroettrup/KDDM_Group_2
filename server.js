"use strict";
// In this file, we write the server implementation

const path = require("path");
const express = require('express');
const app = express();
const port = 3000;
const movies_path = getAbsolutePath("static/data/Movies.json");
const users_path = getAbsolutePath("static/data/users.json");

// Helper functions.
//--------------------------------------------------------------------------------------------

// Returns the absolute string for a given relative string in the current working directory.
function getAbsolutePath(relativePath){ return path.resolve(__dirname,relativePath) }


function compare( a, b ) {
  
    if ( a.entries().next().value[1].averageRating < b.entries().next().value[1].averageRating ){
      return 1;
    }
    if ( a.entries().next().value[1].averageRating > b.entries().next().value[1].averageRating ){
      return -1;
    }
    return 0;
}

//--------------------------------------------------------------------------------------------

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));

//--------------------------------------------------------------------------------------------

app.use(express.static('static'));

//--------------------------------------------------------------------------------------------

app.set('views', getAbsolutePath('static'));
app.set('view engine', 'ejs');

//--------------------------------------------------------------------------------------------

var session = require('express-session');
app.use(session({
    secret: 'Keep it secret',
    name: 'uniqueSessionID',
    saveUninitialized: false,
    resave: false
}));

//--------------------------------------------------------------------------------------------

const fs = require("fs");

var movies;
// An array which containes the movies sorted by score. Every movie is a map with ID:movie.
var moviesArray = [];

fs.readFile(movies_path, "utf8", (err, jsonString) => {
    if (err) {
        console.log("File read failed:", err);
        return;
    }
    movies = JSON.parse(jsonString);
    
    for(var m in movies){
        var movie = new Map();
        movie.set(m, movies[m])
        moviesArray.push(movie);
    }
    moviesArray.sort(compare);
    console.log("Done processing movies, website can be loaded.")
    console.log("movies length> ", moviesArray.length);
});

var users;
fs.readFile(users_path, "utf8", (err, jsonString) => {
    if (err) {
        console.log("File read failed:", err);
        return;
    }
    users = JSON.parse(jsonString);
});


//--------------------------------------------------------------------------------------------

app.get('/', (req, res) => {
    const searchQuery = req.query.query;

    if (searchQuery) {
        const filteredMovies = moviesArray.filter(movie => {
            const movieData = movie.entries().next().value[1];
            const movieTitle = movieData.primaryTitle || '';
            const movieOriginalTitle = movieData.originalTitle || '';
            const movieStartYear = movieData.startYear || '';
            const movieTitleType = movieData.titleType || '';
            const movieGenres = movieData.genres || '';

            const lowerCaseSearchQuery = searchQuery.toLowerCase();
            return (
                movieTitle.toLowerCase().includes(lowerCaseSearchQuery) ||
                movieOriginalTitle.toLowerCase().includes(lowerCaseSearchQuery) ||
                movieStartYear.toString().includes(searchQuery) ||
                movieTitleType.toLowerCase().includes(lowerCaseSearchQuery) ||
                movieGenres.toLowerCase().includes(lowerCaseSearchQuery)
            );
        });

        if (req.query.page == undefined) {
            res.render('index', { Movies: filteredMovies, User: req.session.username, Page: 1 });
        } else {
            res.render('index', { Movies: filteredMovies, User: req.session.username, Page: req.query.page });
        }
    } else {
        if (req.query.page == undefined) {
            res.render('index', { Movies: moviesArray, User: req.session.username, Page: 1 });
        } else {
            res.render('index', { Movies: moviesArray, User: req.session.username, Page: req.query.page });
        }
    }
});

//--------------------------------------------------------------------------------------------

app.get('/404', (req, res) => {
    res.sendfile('static/404.html');
});

//--------------------------------------------------------------------------------------------

app.get('/register', (req, res) => {
    var message;
    res.render('register', {Message: message});
});

app.post('/register', (req, res, next) => {
    var exists = false;
    if (req.body.username == "") {
        exists = true;
        res.render('register', {Message: "Username field can't be empty."});
    } else if (req.body.password == "") {
        exists = true;
        res.render('register', {Message: "Password field can't be empty."});
    } else {
        for(var u in users){
            if(users[u].Username == req.body.username){
                console.log('User already exists');
                exists = true;
                res.render('register', {Message: "Username already exists."});
            }
        }
    }
    
    if(!exists){
        users[Object.keys(users).length] = {
            'Username': req.body.username, 'Password': req.body.password, 'ID': Object.keys(users).length, 'Favorites': []};
        fs.writeFile(users_path, JSON.stringify(users), (err) => {
            if (err)
              console.log(err);
          });
        res.redirect('/login');
    }
});

//--------------------------------------------------------------------------------------------

app.get('/login', (req, res) => {
    var message
    res.render('login', {Message: message});
});

app.post('/login', bodyParser.urlencoded(), (req, res, next) => {
    var logging_in = false;
    var userId;
    var favorites;
    for (var u in users){
        if (req.body.username == users[u].Username) {
            if (req.body.password == users[u].Password) {
                userId = users[u].ID;
                favorites = users[u].Favorites;
                logging_in = true;
            }
        }
    }
    if(!logging_in){
        res.render('login', {'Message': "Username or password incorrect. Please try again."});
    }
    else {
        req.session.userId = userId;
        req.session.favorites = favorites;
        next();
    }
}, (req, res) => {
    req.session.loggedIn = true;
    req.session.username = req.body.username;
    res.redirect('/');
});

app.get('/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/');
});

//--------------------------------------------------------------------------------------------

app.get('/q/:movieId', (req, res) => {
    const movieId = req.params.movieId;
    const movie = movies[movieId];
    res.render('movie', { movie, 'User': req.session.username, 'UserId': req.session.userId, 'Favorites': req.session.favorites });
});

app.post("/update-user/:movieId", (req, res) => {
    const { movieId } = req.params;
    const action = req.query.action;

    if (action === "add") {
        if (!req.session.favorites.includes(movieId)) {
            req.session.favorites.push(movieId);
        }
    } else if (action === "remove") {
        const index = req.session.favorites.indexOf(movieId);
        if (index !== -1) {
            req.session.favorites.splice(index, 1);
        }
    }

    users[req.session.userId].Favorites = req.session.favorites;

    fs.writeFile(users_path, JSON.stringify(users), "utf8", (err) => {
        if (err) {
            console.error("Error updating user data:", err);
            return res.status(500).json({ error: "Internal Server Error" });
        }

        console.log("User data updated successfully");
        return res.status(200).json({ message: "User data updated successfully", Favorites: req.session.favorites });
    });
});



//--------------------------------------------------------------------------------------------

app.get('/about', (req, res) => {
    res.render('about', {'User': req.session.username});
});

app.get('/favorites', (req, res) => {
    const searchQuery = req.query.query;
    if (req.session.favorites) {
        const favoriteMovies = moviesArray.filter(movie => {
            const movieData = movie.entries().next().value[1];
            const movieId = movieData.tconst;
            return req.session.favorites.includes(movieId);
        });
        if (searchQuery) {
            const filteredMovies = favoriteMovies.filter(movie => {
                const movieData = movie.entries().next().value[1];
                const movieTitle = movieData.primaryTitle || '';
                const movieOriginalTitle = movieData.originalTitle || '';
                const movieStartYear = movieData.startYear || '';
                const movieTitleType = movieData.titleType || '';
                const movieGenres = movieData.genres || '';

                const lowerCaseSearchQuery = searchQuery.toLowerCase();
                return (
                    movieTitle.toLowerCase().includes(lowerCaseSearchQuery) ||
                    movieOriginalTitle.toLowerCase().includes(lowerCaseSearchQuery) ||
                    movieStartYear.toString().includes(searchQuery) ||
                    movieTitleType.toLowerCase().includes(lowerCaseSearchQuery) ||
                    movieGenres.toLowerCase().includes(lowerCaseSearchQuery)
                );
            });
            if (req.query.page == undefined) {
                res.render('index', { Movies: filteredMovies, User: req.session.username, Page: 1 });
            } else {
                res.render('index', { Movies: filteredMovies, User: req.session.username, Page: req.query.page });
            }
        } else {
            if (req.query.page == undefined) {
                res.render('favorites', { Movies: favoriteMovies, User: req.session.username, Page: 1 });
            } else {
                res.render('favorites', { Movies: favoriteMovies, User: req.session.username, Page: req.query.page });
            }
        }
    } else {
        res.render('favorites', { Movies: [], User: req.session.username, Page: 1 });
    }
});

//--------------------------------------------------------------------------------------------

app.get('/:anything', (req, res) => {
    res.render('404', {'User': req.session.username});
});

//--------------------------------------------------------------------------------------------

app.listen(port, () => {
    console.log(`KDDM1 app listening at http://localhost:${port}`);
});
