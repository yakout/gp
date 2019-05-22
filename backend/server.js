const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");

const api = require("./routes/api/api");
const app = express();

// Body Parser middleware
app.use(
  bodyParser.urlencoded({
    extended: true
  })
);
app.use(bodyParser.json());

// Use Routes
app.use("/api/", api);

// Serve static assets if in production
if (process.env.NODE_ENV === "production") {
  // Set static folder
  app.use(express.static("client/build"));

  app.get("*", (req, res) => {
    res.sendFile(path.resolve(__dirname, "client", "build", "index.html"));
  });
}

const port = process.env.PORT || 5000;

var server = app.listen(port, () =>
  console.log(`Server started on port ${server.address().port}`)
);
