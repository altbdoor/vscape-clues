(function (d, w) {
	var searchQuery = $('#search-query').attr('disabled', 'disabled').val('');
	
	$.ajax({
		beforeSend: function (request) {
			request.setRequestHeader('Accept', 'application/vnd.github.v3+json');
		},
		dataType: 'json',
		url: 'https://api.github.com/repos/altbdoor/vscape-clues/git/refs/heads/json_data',
	}).then(function (data) {
		var sha = data.object.sha;
		
		$.getJSON('https://api.github.com/repos/altbdoor/vscape-clues/git/commits/' + sha, function (dataJ) {
			var time = Date.parse(dataJ.author.date),
				date = new Date(time);
			
			$('#update-time').text(date.toUTCString());
		});
		
		$.getJSON('//cdn.rawgit.com/altbdoor/vscape-clues/' + sha + '/clue.json', function (data) {
			$(searchQuery).removeAttr('disabled').typeahead({
				source: data,
				items: 10,
				autoSelect: true,
				displayText: function (item) {
					return item.query;
				},
				afterSelect: function (item) {
					var htmlStr = parseItemToHtml(item);
					$('#search-result').html(htmlStr).removeClass('hide');
				},
			}).trigger('focus');
			
		});
	});
	
	function parseItemToHtml (item) {
		var htmlStr = '';
		
		htmlStr += '<div class="row"><div class="col-sm-8">' +
			'<img src="' + item.img_l + '" class="img-responsive img-100">' +
			'</div><div class="col-sm-4">';
		
		if (item.type == 'coordinate' || item.type == 'map') {
			htmlStr += '<img src="' + item.extra.img_mini_l + '" class="img-responsive img-100 mb-10">';
		}
		
		htmlStr += '<b>' + item.query.toUpperCase() + '</b><br>' + item.desc +
			'</div></div>';
		
		return htmlStr;
	}
	
	$('#trigger-credits').one('click', function () {
		$('#credits').removeClass('hide');
	});
})(document, window);
