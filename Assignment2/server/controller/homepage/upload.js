import multer from 'multer';
import fs from 'fs';
import { getUserName } from '../login.js';

// Set up multer storage configuration
const storage = multer.diskStorage({
    destination: (req, file, callback) => {
        const username = getUserName(); // Get the username from the request body
        // console.log("username = " + username)
        const userDirectory = `public/${username}`;
        if(!username) return false;
        // Check if the directory exists, create it if not
        if (!fs.existsSync(userDirectory)) {
            fs.mkdirSync(userDirectory, { recursive: true });
        }

        callback(null, userDirectory);
    },
    filename: (req, file, callback) => {
        callback(null, Date.now() + '_' + file.originalname);
    }
});

const uploadFile = multer({ storage: storage }).single('image');

const uploadFileHandler = (req, res) => {
    try {
        uploadFile(req, res, (err) => {
            if (err) {
                console.error("upload error ", err.message);
                return res.status(500).send(err.message);
            }

            
            if (!req.file) {
                return res.status(400).send('No files were uploaded.');
            }

            // const username =getUserName(); // Get the username from the request body
            // console.log("username = " + username)
            // const filename = Date.now() + '_' + req.file.originalname;
            // const filePath = path.join(`./Database/userData/${username}`, filename);

            // // Save the file to the server
            // fs.renameSync(req.file.path, filePath);
            res.send('File uploaded successfully!');
        });
    } catch (error) {
        console.error("upload error ", error.message);
        res.status(500).send(error.message);
    }
}

export default uploadFileHandler;
