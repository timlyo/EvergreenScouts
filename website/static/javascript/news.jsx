var ArticleBox = React.createClass({
    getInitialState: function(){
        return ({articles: []});
    },
    render: function(){
        return(
            <div>
                <ArticleStats articles={this.props.articles}/>
                <ArticleList articles={this.props.articles}/>
            </div>
        );
    }
 });

var ArticleStats = React.createClass({
    render: function(){
        return(
            <span>
                Count: {this.props.articles}
            </span>
        );
    }
});

var ArticleList = React.createClass({
  render: function() {
    return (
      <p> Test {this.props.articles}</p>
    );
  }
});

var Article = React.createClass({
    render: function(){
        return(
            <p> Article </p>
        );
    }
});

//articles=react.createFragment({
//    [
//        {title: "audv"},
//        {title: "ahdbaifabs"}
//    ]
//);

ReactDOM.render(
  <ArticleBox articles=[
        {title: "audv"},
        {title: "ahdbaifabs"}
    ]}/>,
  document.getElementById('articleBox')
);