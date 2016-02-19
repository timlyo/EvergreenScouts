function get_current_date() {
    var date = new Date();
    return date.toISOString().split("T")[0];
}

var ProgramContainer = React.createClass({
    getInitialState: function() {
        return {programs: [], currentProgram: ""}
    },
    componentDidMount: function() {
        $.ajax({
            url: "/api/program",

            success: function(result) {
                this.setState({programs: result.programs});
            }.bind(this)
        });
    },
    selectProgram: function(event) {
        console.log("selecting program", event.target.value);
        var program = event.target.value;
        this.setState({currentProgram: program});
        console.log(this.state.currentProgram);
    },
    render: function() {
        var options = this.state.programs.map(function(program) {
            return (
                <option>{program["name"]}</option>
            );
        });

        var currentProgram = this.state.currentProgram;
        var program = this.state.programs.filter(function(program) {
            return program.name == currentProgram
        });

        if (program.length == 1) {
            program = program[0];
        }

        console.log("program:", program);
        console.log("Current program:", currentProgram);
        console.log("programs:", this.state.programs);

        return (
            <div>
                <div className="ui form">
                    <div className="field">
                        <select onChange={this.selectProgram}>
                            <option></option>
                            {options}
                        </select>
                    </div>
                </div>
                <Program name={this.state.currentProgram} program={program}/>
            </div>
        )
    }
});

var Program = React.createClass({
    getInitialState: function() {
        return {posting: false, "date": get_current_date(), "activity": "", "notes": ""};
    },
    deleteElement: function(index) {
        this.setState({
            events: this.state.events.filter((_, i) => i != index)
        });
    },
    onDateChange: function(event) {
        this.setState({date: event.target.value});
    },
    onActivityChange: function(event) {
        this.setState({"activity": event.target.value});
    },
    onNotesChange: function(event) {
        this.setState({notes: event.target.value});
    },
    addWeek: function() {
        //TODO validity checking
        let date = this.state.date;
        let activity = this.state.activity;
        let notes = this.state.notes;
        if (activity != "") {
            this.setState({
                events: this.state.events.concat([
                    [date, activity, notes]
                ])
            });
        }
    },
    setPostingStatus: function(state) {
        this.setState({"posting": state});
    },
    deleteAll: function() {
        var setState = this.setState.bind(this, {events: []});
        bootbox.confirm("Are you sure?", function(result) {
            if (result) {
                setState();
            }
        });
    },
    saveProgram: function() {
        let setPostingStatus = this.setPostingStatus;
        setPostingStatus(true);
        console.log(this.state.events);
        $.ajax({
            url: this.props.url,
            type: "POST",
            data: {
                "events": JSON.stringify(this.state.events)
            },
            "dataType": "json",

            success: function(result) {
                console.log("save result:");
                console.log(result);
            },
            complete: function() {
                setPostingStatus(false);
            }
        });
    },
    render: function() {
        var deleteElement = this.deleteElement;

        var weeks = this.props.program.map(function(week, index) {
            return (<Week key={index} date={week[0]} activity={week[1]} notes={week[2]} delete={deleteElement.bind(this, index)}/>);
        });

        var save_button;
        if (this.state.posting) {
            save_button = <a className="btn btn-info" disabled>Saving...</a>;
        } else {
            save_button = <a className="btn btn-info" onClick={this.saveProgram}>Save</a>;
        }

        var week_table;
        if (this.props.program.length == 0) {
            week_table = <p>Nothing here, add something above to begin.</p>
        } else {
            week_table = <WeekTable weeks={weeks}/>
        }

        return (
            <div>
                < WeekForm addWeek={this.addWeek} onDateChange={this.onDateChange} onActivityChange={this.onActivityChange} onNotesChange={this.onNotesChange} date={this.state.date} activity={this.state.activity} notes={this.state.notes} posting={this.state.posting}/>
                {week_table}
                <div className="btn-group">
                    {save_button}
                    <a className="btn btn-info" onClick={this.deleteAll}>
                        Delete All
                    </a>
                    <a className="btn btn-info">
                        Export
                    </a>
                </div>
            </div>
        )
    }
});

var WeekTable = React.createClass({
    render: function() {
        return (
            <table className="ui table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Activity</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    {this.props.weeks}
                </tbody>
            </table>
        );
    }
});

var Week = React.createClass({
    render: function() {
        return (
            <tr key={this.props.index}>
                <td>{this.props.date}</td>
                <td>{this.props.activity}</td>
                <td>{this.props.notes}</td>
                <td>
                    <a onClick={this.props.delete} title="Delete week"><span className="glyphicon glyphicon-trash"/>
                    </a>
                </td>
            </tr>
        )
    }
});

var WeekForm = React.createClass({
    render: function() {
        return (
            <div id="weekForm">
                <form className="form-inline">
                    <fieldset className="form-group">
                        <input type="date" className="form-control" value={this.props.date} onChange={this.props.onDateChange}/>
                        <input type="text" className="form-control" value={this.props.activity} onChange={this.props.onActivityChange} placeholder="Activity"/>
                        <input type="text" className="form-control" value={this.props.notes} onChange={this.props.onNotesChange} placeholder="Notes"/>
                        <input type="button" onClick={this.props.addWeek} value="Add" className="btn btn-info"/>
                    </fieldset>
                </form>
            </div>
        )
    }
});

ReactDOM.render(< ProgramContainer />, document.getElementById("program"))
