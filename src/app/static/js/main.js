$(function() {

    // baseUri needs to be the same as in app.py's app.run(URI)
    // to avoid ajax cross domain issues
    var baseUri = "/raspivideo/movies";
    var pathUri = baseUri + "/path";
    var actionUri = baseUri + "/action";
    var playUri = actionUri + "/play";
    var pauseUri = actionUri + "/play_pause";
    var stopUri = actionUri + "/stop"; 
    var i = 0;

    $("#list_movies").click(function() {
	$("table").append("<thead><tr><th>id</th><th>title</th></tr></thead>");
	$("tbody").empty();
	var deferred = $.getJSON(baseUri);

	deferred.done(function(obj) {
	    $.each(obj.movies, function(index, movie) {
		$("tbody").append("<tr><td><p>" + movie.id
		    + "</p></td><td><p>" + movie.title + "</p></td>"
		    + '<td><button class="' + 'btn btn-primary btn-sm' +
		    '" id=' + '"play' + movie.id + '">play</button></td></tr>');

		$("#play" + movie.id).click(function() { 
		    var def = $.getJSON(playUri + "/" + movie.id);
		    def.done(function(obj) {
		    });
		    def.fail(function() {
		    });
		});
	    });
	});
	deferred.fail(function() {
	});
    });

    $("#path_btn").click(function() {
	var path_value = $("#path_value").val();
	var path_data_json = '{ "path": ' + '"' + path_value + '"' + ' }'	
	$.ajax({
	    type: "POST",
	    url: pathUri,
	    data: path_data_json,
	    success: function(data) {},
	    contentType: "application/json",
	    dataType: "json"
	});
    });


    $("#pause").click(function() {
    if ($(this).text() === "play") {
        $(this).text('pause');
    } else {
        $(this).text('play');
    }
    

	var deferred = $.getJSON(pauseUri);
	deferred.done(function(obj) {
	});
	deferred.fail(function() {
	});
    });
    $("#stop").click(function() {
	var def2 = $.getJSON(stopUri);
	def2.done(function(obj) {
	});
	def2.fail(function() {
	});
    });
});
//@ sourceURL=main.js

