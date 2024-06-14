import makeDir from "../Database/createDirectory.js";
import readUserFromFile from "../Database/readFromFile.js";
import writeUserToFile from "../Database/writeTofile.js";

const signUpUser = async (req, res) => {
    const { username, password } = req.body;
    const users = await readUserFromFile();
    const existingUser = users.find(user => user.username === username);

    if (existingUser) {
        // return res.status(400).send(`
        //         <div style="font-family: Arial, sans-serif; color: #721c24; background-color: #f8d7da; border-color: #f5c6cb; padding: 10px; margin: 10px 0; border: 1px solid transparent; border-radius: .25rem;">
        //         User already exists!
        //     </div>
        //     `);
        console.log('Existing user')
        res.redirect("/login");
    }
    else {
        const newUser = {
            username: username,
            password: password
        }

        users.push(newUser);
        await writeUserToFile(users);
        makeDir(res,username);    
        return res.status(200).send(`
            <div style="font-family: Arial, sans-serif; color: #155724; background-color: #d4edda; border-color: #c3e6cb; padding: 10px; margin: 10px 0; border: 1px solid transparent; border-radius: .25rem;">
                Sign-up successful, ${newUser.username}!
            </div>
        `);
    }
}

export default signUpUser;