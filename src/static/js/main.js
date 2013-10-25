$(function() {

    // baseUri needs to be the same as in app.py's app.run(URI)
    // to avoid ajax cross domain issues
    var baseUri = "http://10.0.1.5:5000/raspivideo/movies";
    var actionUri = baseUri + "/action";
    var playUri = actionUri + "/play";
    var pauseUri = actionUri + "/pause";
    var stopUri = actionUri + "/stop"; 
    alert(playUri);

    $("#list_movies").click(function() {
	$("table").append("<thead><tr><th>id</th><th>title</th></tr></thead>");
	//$("tbody").empty();
	//alert("btn clicked");
	var deferred = $.getJSON(baseUri);

	deferred.done(function(obj) {
	    //alert("get succeeded");
	    $.each(obj.movies, function(index, movie) {
		$("tbody").append("<tr><td><p>" + movie.id
		    + "</p></td><td><p>" + movie.title + "</p></td>"
		    + '<td><button class="' + 'btn btn-primary btn-sm' +
		    '" id=' + '"play' + movie.id + '">play</button></td></tr>');

		$("#play" + movie.id).click(function() { 
		    alert("play clicked: " + playUri + "/" + movie.id);
		    var def = $.getJSON(playUri + "/" + movie.id);
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
    $("#pause").click(function() {
	var deferred = $.getJSON(pauseUri);
	deferred.done(function(obj) {
	    alert("pause call succeeded");
	});
	deferred.fail(function() {
	    alert("pause call failed");
	});
    });
});
//@ sourceURL=main.js

