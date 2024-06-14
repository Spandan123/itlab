import express from "express"
import signUpUser from "../controller/signup.js";
import logInUser, { getUserName } from "../controller/login.js";
import authenticate from "../controller/authentication.js";
import uploadFileHandler from "../controller/homepage/upload.js";
import homepageViewer from "../controller/homepage.js";
import deleteFileHandler from "../controller/homepage/delete.js";
import viewFileHandler from "../controller/homepage/view.js";
import downloadFileHandler from "../controller/homepage/download.js";

const router = express.Router();

router.get("/", async (req, res) => {
    try {
         res.render("index.ejs");
    } catch (error) {
        console.log(error.response.data);
        res.status(500);
    }
});

router.get("/signup", async (req, res) => {
    try {
         res.render("signup.ejs");
    } catch (error) {
        console.log(error.response.data);
        res.status(500);
    }
});

router.get("/login", async (req, res) => {
    try {
        res.render("login.ejs");
    } catch (error) {
        console.log(error.response.data);
        res.status(500);
    }
});
router.get("/homepage",homepageViewer);

const username = getUserName();


router.post('/signup', signUpUser);
router.post('/login', authenticate, logInUser);

router.get('/homepage/view',viewFileHandler);
router.get('/homepage/download',downloadFileHandler);

router.post('/homepage/upload',uploadFileHandler);
router.post('/homepage/delete',deleteFileHandler);



export default router;
