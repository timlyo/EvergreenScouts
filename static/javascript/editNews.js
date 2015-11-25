'use strict';

function deleteNews(id) {
    var r = confirm("Are you sure you want to delete this article?");
    console.log(r);
    console.log(id);

    $.post("/news/" + id + "/delete", null, function (data, testStatus, jqXHR) {
        data = JSON.parse(data);
        if (data.success) {
            console.log("ok");
            window.location.replace("/admin");
        }else{
            console.log("probs");
            alert("Error, failed to delete\n data");
        }
    });
}

function restoreNews(id) {
    var r = confirm("Are you sure you want to restore this article?");
    console.log(r);
    console.log(id);

    $.post("/news/" + id + "/restore", null, function (data, testStatus, jqXHR) {
        data = JSON.parse(data);
        if (data.success) {
            console.log("ok");
            window.location.replace("/admin");
        }else{
            console.log("probs");
            alert("Error, failed to restore\n data");
        }
    });
}

function publishNews(id) {
    var r = confirm("Are you sure you want to restore this article?");
    console.log(r);
    console.log(id);

    $.post("/news/" + id + "/publish", null, function (data, testStatus, jqXHR) {
        data = JSON.parse(data);
        if (data.success) {
            console.log("ok");
            window.location.replace("/admin");
        }else{
            console.log("probs");
            alert("Error, failed to restore\n data");
        }
    });
}