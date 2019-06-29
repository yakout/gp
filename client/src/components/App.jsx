import React, { Component } from "react";

import SearchBar from "./SearchBar";
import VideoModule from "./videos/VideoModule";
import socketIOClient from "socket.io-client";

const socket = socketIOClient("http://127.0.0.1:5000");

class App extends Component {
  //* App state
  constructor(props) {
    super(props);
    this.state = {
      videos: [], // List of highlight videos (or ranges from the original video) returned from api call to display in a table
      video_url: null, // Current video being displayed
      processing: false // Flag to indicate if system is currently processing a game
    };
  }

  //* Set default search term
  componentDidMount() {
    this.onSearchSubmit("liv-vs-ars.mp4");
    const { endpoint } = this.state;
    socket.on("receive_highlights", data => this.setState({ videos: [...this.state.videos, data] }));
    socket.on("receive_highlight_reel", res => {
      this.setState({ processing: false,  video_url: res});
    })
  }

  //* User enters a search term
  onSearchSubmit = video_url => {
    this.setState({
      video_url: video_url
    });
  };

  onDetectHighlightsClick = () => {
    const { video_url } = this.state;
    console.log(video_url);
    this.setState({ processing: true });
    socket.emit('generate_highlights', { chunk_duration: 300, video_path: `videos/${video_url}`, duration_limit: 10});
  };

  //[(Callback)] User selected video
  onVideoSelect = video => {
    this.setState({
      video_url: video
    });
  };

  render() {
    const { processing, videos, video_url } = this.state;
    console.log(videos);
    console.log(video_url);
    return (
      <div className="app ui container">
        <SearchBar onSearchSubmit={this.onSearchSubmit} />
        <VideoModule
          appState={this.state}
          onVideoSelect={this.onVideoSelect}
          onDetectHighlightsClick={this.onDetectHighlightsClick}
        />

        {processing ? <h2>Currently Processing...</h2> : <div />}
      </div>
    );
  }
}

export default App;
