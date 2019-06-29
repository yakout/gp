import React, { Component } from "react";
import VideoDetail from "./VideoDetail";
import HighlightsTable from "./HighlightsTable";

class VideoModule extends Component {

  constructor(props) {
    super(props);
    this.state = {
      start_time: 0,
      end_time: -1
    };

    this.onPlayHighlightClick = this.onPlayHighlightClick.bind(this);
  }

  onPlayHighlightClick(start_time, end_time) {
    this.setState({start_time, end_time});
  }

  render() {
    console.log(this.state);
    const { start_time, end_time } = this.state;
    const { video_url, videos } = this.props.appState;
    return (
      <div className="ui grid">
        <div className="ui row">
          <div className="eleven wide column">
            <VideoDetail
              video_url={video_url}
              start_time={start_time}
              end_time={end_time}
              onDetectHighlightsClick={this.props.onDetectHighlightsClick}
            />
          </div>
          <div className="five wide column">
            <HighlightsTable videos={videos} onPlayHighlightClick={this.onPlayHighlightClick}/>
          </div>
        </div>
      </div>
    );
  }
}

export default VideoModule;
