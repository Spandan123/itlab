import fs from 'fs/promises';

const makeDir = async (res,username) => {
  try
    {const dirPath = `public/${username}`;
    fs.mkdir(dirPath,{recursive:true},(err)=>{
        if (err) {
            console.error(`Error creating directory for ${username}:`, err);
          } else {
            console.log(`Directory created for ${username} at ${directoryPath}`);
          }
    });}
    catch(error)
    {
      res.status(400).send(`Error while creating user directory: ${error.message}`)
      console.error("Error while creating user directory: "+error.message);
    }

};

export default makeDir;