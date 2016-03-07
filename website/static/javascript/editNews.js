console.log("Loaded editNews.js");

/**
 * Updates the articles information on the server
 * @param id: id of the article to update
 */
function submit_edit_news_form(id){
    var data = $("#editNewsForm").serializeArray();
    var url = "/api/news/" + id;

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function(response){
            console.log("Success");
            $.notify("Success", "success");
        },
        error: function () {
            console.log("Error");
        }
    });
}


function create_new_article(){
    var url = "/api/news";
    console.log("new Article");

    $.ajax({
        type: "POST",
        url: url,
        success: function(response){
            console.log("Success");
            $.notify("saved", "success");
        },
        error: function () {
            console.log("Error");
        }
    });
}