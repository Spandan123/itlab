let userName = '';

export const logInUser = async (req, res) => {
    try {
        userName = req.session.username;
        console.log(`Welcome back, ${userName}!`);
        res.redirect(`/homepage`);
    } catch (error) {
        console.error("Error reading user data:", error.message);
        res.status(500).send("Internal Server Error");
    }
};

export const getUserName = () => {
    return userName;
};

export default logInUser;
