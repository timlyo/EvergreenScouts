function get_current_date() {
    var date = new Date();
    return date.toISOString().split("T")[0];
}

var Program = React.createClass({
    getInitialState: function () {
        return {
            events: [],
            name: "",
            posting: false
        };
    },
    componentDidMount: function () {
        $.ajax({
            url: this.props.url,

            success: function (data) {
                this.setState(data);
            }.bind(this),

            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    addWeek: function () {
        this.setState({events: this.state.events.concat([["Date", "Event", "Notes"]])});
    },
    saveProgram: function () {
        this.state.posting = true;
        console.log(this.state.events);
        $.ajax({
            url: this.props.url,
            type: "POST",
            data: {"events": JSON.stringify(this.state.events)},
            "dataType": "json",

            success: function (result) {
                console.log(result);
            }
        });
    },
    render: function () {
        var weeks = this.state.events.map(function (week, index) {
            return (
                <tr key={index}>
                    <td>{week[0]}</td>
                    <td>{week[1]}</td>
                    <td>{week[2]}</td>
                </tr>
            );
        });

        return (
            <div>

                < WeekForm addWeek={this.addWeek}/>
                <br/>
                <table className="table">
                    <tbody>
                    {weeks}
                    </tbody>

                </table>
                <br/>
                <a className="btn btn-info" onClick={this.saveProgram}>Save</a>
            </div>
        )
    }
});

var WeekForm = React.createClass({
    getInitialState: function () {
        return {
            "date": get_current_date(),
            "activity": "",
            "notes": ""
        }
    },
    render: function () {
        return (
            <div id="weekForm">
                <form className="form-inline">
                    <fieldset className="form-group">
                        <input type="date" className="form-control" value={this.state.date}/>
                        <input type="text" className="form-control" value={this.state.activity} placeholder="Activity"/>
                        <input type="text" className="form-control" value={this.state.notes} placeholder="Notes"/>
                        <input type="button" onClick={this.props.addWeek} value="Add" className="btn btn-info"/>
                    </fieldset>
                </form>
            </div>
        )
    }
});

let url = "/api/program?name=" + programName;
console.log(url);

ReactDOM.render(
    <Program url={url}/>,
    document.getElementById("program")
)