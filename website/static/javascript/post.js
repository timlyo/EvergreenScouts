function save_article(data, id){
    console.log(data);
    $.ajax({
        url:"/api/news/" + id,
        data: data,
        success: function(){
            console.log("Success");
        },
        error: function () {
            console.log("Error");
        }
    })
}