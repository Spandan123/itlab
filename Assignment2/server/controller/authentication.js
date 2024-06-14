import readUserFromFile from "../Database/readFromFile.js";
const authenticate = async (req, res, next) => {
    const username = req.body.username;
    const password = req.body.password;

    try {
        const users = await readUserFromFile();
        const existingUser = users.find(user => user.username === username);

        if (existingUser) {
            if (password === existingUser.password) {
                console.log("Authentication successful by authenticator");

                // Set session variables
                req.session.isAuthenticated = true;
                req.session.username = username;
                res.status(200);
                next(); // Continue to the next middleware or route handler
            } else {
                console.log("Incorrect password");
                req.session.isAuthenticated = false;
                next(); // Continue to the next middleware or route handler
            }
        } else {
            console.log("User not found:", username);
            req.session.isAuthenticated = false;
            next(); // Continue to the next middleware or route handler
        }
    } catch (error) {
        console.error("Error reading user data:", error.message);
        res.status(500).send("Internal Server Error");
    }
};

export default authenticate;