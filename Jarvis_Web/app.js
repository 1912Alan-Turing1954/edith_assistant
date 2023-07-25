const express = require('express');
const { exec } = require('child_process');
const app = express();

// Endpoint to render the EJS template
app.get('/', (req, res) => {
  // Execute the Python script
    exec('python ./', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing the Python script: ${error}`);
        res.status(500).send('Error executing the Python script.');
        return;
    }

    // Assuming the Python script outputs the result you want to display
    const result = stdout;

    // Render the EJS template with the Python script result
    res.render('index', { result });
    });
});

// Start the server
const port = 3000;
app.listen(port, () => {
    console.log(`Server started on http://localhost:${port}`);
});
