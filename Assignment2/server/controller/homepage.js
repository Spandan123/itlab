import fs from 'fs';
import path from 'path';
import { getUserName } from './login.js';

const homepageViewer = async (req, res) => {
    try {
        const username = getUserName()
        if (req.session.isAuthenticated) {
            console.log("user name = " + username);
            const userDirectory = `public/${username}`;
            const images = fs.readdirSync(userDirectory)
                .filter(file => file.toLowerCase())
                .map(file => {
                    const imagePath = path.join(userDirectory, file);
                    const stats = fs.statSync(imagePath);
                    return {
                        filename: file,
                        path: imagePath,
                        size: stats.size,
                        lastModified: stats.mtime
                    };
                });
            res.render('homepage2.ejs', { images, username });

        } else {
            console.log("Authentication failed");
            res.status(401).send("Authentication failed");
        }

    }
    catch (error) {
        console.error('Error in homepageViewer:', error);

        // Handle the error appropriately, send an error response, redirect, or render an error page
        res.status(500).send('Internal Server Error');
    }
};

export default homepageViewer;
