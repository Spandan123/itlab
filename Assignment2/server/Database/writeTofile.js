import path from 'path';
import fs from 'fs/promises'


const userFilePath = path.join('Database', "userId.json");

const writeUserToFile = async (users) => {
    try {
        await fs.writeFile(userFilePath, JSON.stringify(users, null, 2));
    } catch (error) {
        console.error('Error writing users file:', error.message);
    }
};

export default writeUserToFile;