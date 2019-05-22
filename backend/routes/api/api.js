const express = require("express");
const router = express.Router();
const exec = require("child_process").exec;

const detect = cmd => {
  console.log(`Command to execute: ${cmd}`);
  return new Promise((resolve, reject) => {
    exec(cmd, { maxBuffer: 500 * 1024 }, (error, stdout, stderr) => {
      if (error) {
        console.log("Error found in exec");
        console.log(error);
        return reject(error);
      }
      console.log(`stderr: ${stderr}`);
      console.log(`stdout: ${stdout}`);
      return resolve(true);
    });
  });
};

// @route   POST api/detect
// @desc    Given a video url of the game, detects highlights of the game and returns the url of the highlight reel
// @access  Public
router.post("/detect", (req, res) => {
  console.log(req.body);

  const video_path = "videos/" + req.body.video_url;
  const cmd = `python3.7 main.py ${video_path} 120 0`;
  // run python command using a promise, and return the name of the output to the frontend.
  detect(cmd)
    .then(result => {
      if (result === true) {
        console.log("Executed command successfully!");
        return res.json({ output_path: "output/output_120_secs.mp4" });
      }
      console.log("result is not true :(");
    })
    .catch(err => {
      console.log(err);
      res.status(400).json(err);
    });
});

module.exports = router;
