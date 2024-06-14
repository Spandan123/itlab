import express from 'express';
import path from 'path';
import fs from 'fs';

const app = express();

function decodePath(encodedPath) {
    return decodeURIComponent(encodedPath);
}

const downloadFileHandler = async (req, res) => {
    try {
        const filePath = decodePath(req.query.imagePath);
        const imagePath = path.resolve('./public', filePath);

        console.log("path == " + filePath);
        console.log("absolute == " + imagePath);

        // Check if the file exists
        if (!fs.existsSync(imagePath)) {
            console.error('File not found:', imagePath);
            res.status(404).send('File Not Found');
            return;
        }

        // Set headers for download
        res.setHeader('Content-disposition', `attachment; filename=${path.basename(imagePath)}`);
        res.setHeader('Content-type', 'image/jpeg'); // Adjust the content-type based on your file type

        // Use res.sendFile for simplicity
        res.sendFile(imagePath, (err) => {
            if (err) {
                console.error('Error sending file:', err);
                res.status(500).send('Internal Server Error');
            } else {
                console.log('File sent successfully');
            }
        });

    } catch (error) {
        console.error("Download error ", error.message);
        res.status(500).send("Error: " + error.message);
    }
};

export default downloadFileHandler;