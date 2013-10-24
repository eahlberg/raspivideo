$(function() {
    var baseUri = "http://localhost:5000/raspivideo/movies";

    $("#list_movies").click(function() {
        $("tbody").empty();
        $("table").append("<thead><tr><th>id</th><th>title</th></tr></thead>");
        var deferred = $.getJSON(baseUri);

        deferred.done(function(obj) { 
            $.each(obj.movies, function(index, movie) {
                $("tbody").append("<tr><td>" + movie.id
                    + "</td><td>" + movie.title + "</td></tr>");
            });
        });
        deferred.fail(function() {
            console.log("fail");
        });
    });
});

//@ sourceURL=main.js
