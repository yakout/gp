import React, { Component } from "react";
import "./App.css";
import VideoDisplay from "./components/VideoDisplay";

class App extends Component {
  render() {
    return (
      <div className="App">
        <VideoDisplay />
      </div>
    );
  }
}

export default App;
