import path from 'path';

const viewFileHandler = async (req, res) => {
    try {
        const filePath = req.query.imagePath;
        console.log("path == " + filePath);
        const imagePath = path.join('../', filePath);

        console.log("absolute == " + imagePath);

      
        res.render('viewFile.ejs',{imagePath});
    } catch (error) {
        console.error("upload error ", error.message);
        res.status(500).send(error.message);
    }
};

export default viewFileHandler;
