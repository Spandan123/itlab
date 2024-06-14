import { promises as fsPromises } from 'fs';
import path from 'path';


function decodePath(encodedPath) {
    return decodeURIComponent(encodedPath);
}

const deleteFileHandler = async(req, res) => {
    try {
        const filePath = decodePath(req.body.imagePath);
        const imagePath = path.resolve('./public', filePath);
        console.log("path == "+imagePath)
        await fsPromises.unlink(imagePath);
        res.status(200).send("FIle deleted successfully")
    } catch (error) {
        console.error("upload error ", error.message);
        res.status(500).send(error.message);
    }
}

export default deleteFileHandler;
