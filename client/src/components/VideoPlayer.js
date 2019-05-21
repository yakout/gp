import React, { Component } from "react";
import { Player } from "video-react";

const video_url = "http://www.w3schools.com/html/mov_bbb.mp4";

class VideoPlayer extends Component {
  render() {
    return (
      <div className="video-detail col-md-8">
        <div className="embed-responsive embed-responsive-16by9">
          <Player src={video_url} fluid={false}>
            {/* <source  /> */}
          </Player>
        </div>
      </div>
    );
  }
}

export default VideoPlayer;
