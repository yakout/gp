import React, { Component } from "react";
import axios from "axios";

import SearchBar from "./SearchBar";
import VideoModule from "./videos/VideoModule";

class App extends Component {
  //* App state
  state = {
    videos: [], // List of highlight videos (or ranges from the original video) returned from api call to display in a table
    video_url: null, // Current video being displayed
    processing: false // Flag to indicate if system is currently processing a game
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

  onDetectHighlightsClick = () => {
    const { video_url } = this.state;
    console.log(video_url);
    this.setState({ processing: true });
    axios
      .post("/api/detect", { video_url })
      .then(res => {
        console.log(res);
        this.setState({ video_url: res.data.output_path, processing: false });
      })
      .catch(err => {
        console.log(err);
      });
  };

  //[(Callback)] User selected video
  onVideoSelect = video => {
    this.setState({
      video_url: video
    });
  };

  render() {
    const { processing } = this.state;
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
