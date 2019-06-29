import React, { Component } from "react";
import BootstrapTable from "react-bootstrap-table-next";

class HighlightsTable extends Component {
  constructor(props) {
    super(props);
  }

  play(row) {
    console.log(row);
  }

  playFormatter(cell, row, rowIndex, formatExtraData) {
    return (
      <button
        onClick={() => formatExtraData.src.play(row)}
      >
        <i className="play circle icon"></i>
      </button>
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
