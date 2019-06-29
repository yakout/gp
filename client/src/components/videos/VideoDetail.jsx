import React, { Component } from "react";
import ReactPlayer from 'react-player'

const example_url =
  "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4";

class VideoDetail extends Component {
  constructor(props) {
    super(props);

    this.state = {
      playing: true
    };

    this.getTitle = this.getTitle.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
    this.onProgress = this.onProgress.bind(this);
  }

  getTitle = video_url => {
    const slashIdx = video_url.lastIndexOf("/");
    return slashIdx === -1
      ? video_url.substring(0, video_url.lastIndexOf("."))
      : video_url.substring(slashIdx + 1, video_url.lastIndexOf("."));
  };

  onSubmit = e => {
    e.preventDefault();
    this.props.onDetectHighlightsClick();
  };

  onProgress = playerState => {
    const { playedSeconds } = playerState;
    // console.log(playedSeconds);
    if (this.props.end_time !== -1 && playedSeconds > this.props.end_time) {
      this.setState({playing: false});
    }
  };

  render() {
    const { video_url } = this.props;
    if (!video_url) {
      return <div>Loading...</div>;
    }
    const title = this.getTitle(video_url);
    console.log(`Received video url: ${video_url}`);
    console.log(`Video Title: ${title}`);

    const { start_time, end_time } = this.props;
    console.log(this.props);
    console.log(start_time);
    console.log(end_time);

    return (
      <div>
        <div className="video-detail">
          <ReactPlayer
            url={video_url}
            controls
            width='100%'
            height='100%'
            playing={this.state.playing}
            ref={player => {
              if (player !== null) {
                player.seekTo(start_time, 'seconds')
              }
            }}
            onProgress={this.onProgress}
          />
        </div>
        <div className="ui segment">
          <h2 className="ui header">{title}</h2>
          <button className="ui button" onClick={this.onSubmit}>
            Start Highlight Detection
          </button>
        </div>
      </div>
    );
  }
}

export default VideoDetail;
