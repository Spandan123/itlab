
import express from 'express';
import router from './Route/route.js';
import {EventEmitter} from 'events';
import session from 'express-session';
import path from 'path'

EventEmitter.defaultMaxListeners = 15; 
const app = express();
const port = 9000;
app.use(express.json())
app.use(express.urlencoded({ extended: true }));
app.use('/Database', express.static(path.join('/controller', '../Database/userData')));

app.set("view engine" ,"ejs");
app.use(session({
  secret: 'your-secret-key', // Change this to a secure random key
  resave: false,
  saveUninitialized: true,
}));
app.use(express.static('public'))
app.use('/',router);


app.listen(port, () => {
    console.log(`server is listening on port: ${port}`);
});

process.removeAllListeners('exit');

process.on('warning', (warning) => {
  console.warn(warning.stack);
});