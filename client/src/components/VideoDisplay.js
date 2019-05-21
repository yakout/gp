import React, { Component } from "react";
import VideoEntry from "./VideoEntry";
import VideoPlayer from "./VideoPlayer";

class VideoDisplay extends Component {
  render() {
    return (
      <div>
        <VideoEntry />
        <VideoPlayer />
      </div>
    );
  }
}

export default VideoDisplay;
