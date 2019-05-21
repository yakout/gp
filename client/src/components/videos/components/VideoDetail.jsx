import React, { Component } from "react";
import { Embed } from "semantic-ui-react";

const example_url =
  "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4";

class VideoDetail extends Component {
  constructor(props) {
    super(props);

    this.getTitle = this.getTitle.bind(this);
  }

  getTitle(video_url) {
    const slashIdx = video_url.lastIndexOf("/");
    return slashIdx === -1
      ? video_url.substring(0, video_url.lastIndexOf("."))
      : video_url.substring(slashIdx + 1, video_url.lastIndexOf("."));
  }

  render() {
    const { video_url } = this.props;
    if (!video_url) {
      return <div>Loading...</div>;
    }
    const title = this.getTitle(video_url);

    return (
      <div>
        <div className="video-detail">
          <Embed icon="video" url={video_url} />
        </div>
        <div className="ui segment">
          <h2 className="ui header">{title}</h2>
          <button className="ui button">Start Highlight Detection</button>
        </div>
      </div>
    );
  }
}

export default VideoDetail;
