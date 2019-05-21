import React, { Component } from "react";

class VideoEntry extends Component {
  render() {
    return (
      <div className="search-bar">
        <input type="text" name="video_path" placeholder="Enter video path" />
      </div>
    );
  }
}

export default VideoEntry;
