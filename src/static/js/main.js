$(function() {

    // baseUri needs to be the same as in app.py's app.run(URI)
    // to avoid ajax cross domain issues
    var baseUri = "http://0.0.0.0:5000/raspivideo/movies";
    var playUri = "play";

    $("#list_movies").click(function() {
        $("tbody").empty();
        $("table").append("<thead><tr><th>id</th><th>title</th></tr></thead>");
        alert("btn clicked");
        var deferred = $.getJSON(baseUri);

        deferred.done(function(obj) {
            alert("get succeeded");
            $.each(obj.movies, function(index, movie) {
                $("tbody").append("<tr><td>" + movie.id
                    + "</td><td>" + movie.title + "</td>"
                    + '<td><button id="play' + movie.id + '">play</button></td></tr>');
                $("#play" + movie.id).click(function() { 
                    var def = $.getJSON(baseUri + "/" + playUri + "/" + movie.id);
                    def.done(function(obj) {
                        console.log("sending play request");
                    });
                    def.fail(function() {
                        console.log("fail in play request");
                    });
                });
            });
        });
        deferred.fail(function() {
            console.log("fail");
        });
    });
});

//@ sourceURL=main.js
