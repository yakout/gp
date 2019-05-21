import React, { Component } from "react";

import SearchBar from "./SearchBar";
import VideoModule from "./videos/VideoModule";

class App extends Component {
  //* App state
  state = {
    videos: [],
    video_url: null
  };

  //* Set default search term
  componentDidMount() {
    this.onSearchSubmit("liv-vs-ars.mp4");
  }

  //* User enters a search term
  onSearchSubmit = video_url => {
    this.setState({
      video_url: video_url
    });
  };

  //[(Callback)] User selected video
  onVideoSelect = video => {
    this.setState({
      video_url: video
    });
  };

  render() {
    return (
      <div className="app ui container">
        <SearchBar onSearchSubmit={this.onSearchSubmit} />
        <VideoModule appState={this.state} onVideoSelect={this.onVideoSelect} />
      </div>
    );
  }
}

export default App;
