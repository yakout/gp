import React, { Component } from "react";
import BootstrapTable from "react-bootstrap-table-next";

class HighlightsTable extends Component {
  constructor(props) {
    super(props);

    this.getTimeInSeconds = this.getTimeInSeconds.bind(this);
  }

  getTimeInSeconds = time => {
    const arr = time.split(":");
    var totalTime = 0;
    totalTime += 3600 * parseInt(arr[0]);
    totalTime += 60 * parseInt(arr[1]);
    totalTime += parseInt(arr[2]);
    return totalTime;
  };

  play(row) {
    this.props.onPlayHighlightClick(this.getTimeInSeconds(row[0]), this.getTimeInSeconds(row[1]));
  }

  playFormatter(cell, row, rowIndex, formatExtraData) {
    return (
        <i className="play circle icon" onClick={() => formatExtraData.src.play(row)}></i>
    );
  }

  columns = [
    {
      dataField: "0",
      text: "Start",
      classes: "grey-text text-center"
    },
    {
      dataField: "1",
      text: "End",
      classes: "grey-text text-center"
    },
    {
      dataField: "2",
      text: "Score",
      classes: "grey-text text-center"
    },
    {
      dataField: "playButton",
      text: "Play",
      formatter: this.playFormatter,
      formatExtraData: {
        src: this
      }
    }
  ];

  render() {
    console.log(this.props.videos);
    return (
      <div>
        <BootstrapTable
              keyField="Index"
              data={this.props.videos}
              columns={this.columns}
              hover
              condensed
              bordered={false}
              condensed
              // pagination={paginationFactory(this.options)}
              // filter={filterFactory()}
            />
      </div>
    );
  }
}

export default HighlightsTable;
