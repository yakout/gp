import React, { Component } from "react";
import VideoDetail from "./components/VideoDetail";
import VideosList from "./components/VideosList";
import HighlightsTable from "./HighlightsTable";

class VideoModule extends Component {
  render() {
    const { video_url, videos } = this.props.appState;
    return (
      <div className="ui grid">
        <div className="ui row">
          <div className="eleven wide column">
            <VideoDetail
              video_url={video_url}
              onDetectHighlightsClick={this.props.onDetectHighlightsClick}
            />
          </div>
          <div className="five wide column">
            <HighlightsTable videos={videos}/>
          </div>
        </div>
      </div>
    );
  }
}

export default VideoModule;
