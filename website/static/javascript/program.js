function get_current_date() {
    var date = new Date();
    return date.toISOString().split("T")[0];
}

var Program = React.createClass({
    getInitialState: function () {
        return {
            events: [],
            name: "",
            posting: false,
            "date": get_current_date(),
            "activity": "",
            "notes": ""
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
    deleteElement: function(index, event){
        this.setState({
            events: this.state.events.filter((_, i) => i != index)
        });
    },
    onDateChange: function (event) {
        this.setState({date: event.target.value});
    },
    onActivityChange: function (event) {
        this.setState({"activity": event.target.value});
    },
    onNotesChange: function (event) {
        this.setState({notes: event.target.value});
    },
    addWeek: function () {
        //TODO validity checking
        let date = this.state.date;
        let activity = this.state.activity;
        let notes = this.state.notes;
        this.setState({events: this.state.events.concat([[date, activity, notes]])});
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
        var deleteElement = this.deleteElement;
        var weeks = this.state.events.map(function (week, index) {
            return (
                <Week
                    key={index} date={week[0]} activity={week[1]} notes={week[2]}
                    delete={deleteElement.bind(this, index)}
                />
            );
        });

        return (
            <div>
                < WeekForm addWeek={this.addWeek}
                           onDateChange={this.onDateChange} onActivityChange={this.onActivityChange} onNotesChange={this.onNotesChange}
                           date={this.state.date} activity={this.state.activity} notes={this.state.notes}/>
                <br/>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Activity</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
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

var Week = React.createClass({
    render: function(){
        return(
            <tr key={this.props.index}>
                <td>{this.props.date}</td>
                <td>{this.props.activity}</td>
                <td>{this.props.notes}</td>
                <td><a onClick={this.props.delete}><span className="glyphicon glyphicon-trash" /> </a></td>
            </tr>
        )
    }
});

var WeekForm = React.createClass({
    render: function () {
        return (
            <div id="weekForm">
                <form className="form-inline">
                    <fieldset className="form-group">
                        <input type="date" className="form-control" value={this.props.date}
                               onChange={this.props.onDateChange}/>
                        <input type="text" className="form-control" value={this.props.activity}
                               onChange={this.props.onActivityChange} placeholder="Activity"/>
                        <input type="text" className="form-control" value={this.props.notes}
                               onChange={this.props.onNotesChange} placeholder="Notes"/>
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