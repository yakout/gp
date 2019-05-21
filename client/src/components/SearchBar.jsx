import React, { Component } from "react";
import "../styles/SearchBar.scss";

class SearchBar extends Component {
  constructor(props) {
    super(props);

    this.state = {
      video_url: ""
    };

    this.onFormSubmit = this.onFormSubmit.bind(this);
    this.onInputChange = this.onInputChange.bind(this);
  }

  // User hits enter on search
  onFormSubmit = event => {
    event.preventDefault();
    console.log(this.state.video_url);

    this.props.onSearchSubmit(this.state.video_url);
  };

  // Set the value of search bar
  onInputChange = event => {
    const { value, name } = event.target;
    this.setState({
      [name]: value
    });
  };

  render() {
    const { video_url } = this.state;
    return (
      <div className="search-bar ui segment">
        <form className="ui form" onSubmit={this.onFormSubmit}>
          <div className="field">
            <label htmlFor="search-bar-input">Video Path</label>
            <input
              id="search-bar-input"
              type="text"
              name="video_url"
              value={video_url}
              onChange={this.onInputChange}
              placeholder="Enter video path"
            />
          </div>
        </form>
      </div>
    );
  }
}

export default SearchBar;
