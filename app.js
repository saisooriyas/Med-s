const express = require('express');
const cors = require('cors');
const app = express();

// allow requests from all domains
app.use(cors());

// your server routes and logic here
// ...

app.listen(5005, () => {
    console.log('Server listening on port 5005');
});
