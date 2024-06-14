import path from 'path';
import fs from 'fs/promises'

const userFilePath = path.join('Database', "userId.json");

const readUserFromFile = async () => {
    try {
        const usersData = await fs.readFile(userFilePath, 'utf8');
        console.log('Raw users data:', usersData);
        return JSON.parse(usersData);
    } catch (error) {
        console.error('Error reading users file:', error.message);
        return [];
    }
};

export default readUserFromFile;