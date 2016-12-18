$('.js-like-question').on('click', function() {
	var $btn = $(this);
	$.ajax({
		url: '/like_question/',
		method: 'POST',
		data: {
			id: $btn.data('id'),
			type: $btn.data('type'),
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
		}
	}).done(function(resp) {
		if(resp && resp.status == 'ok') 
		{
			window.location.reload();
		}
	})
	return false;
});

$('.js-like-answer').on('click', function() {
	var $btn = $(this);
	$.ajax({
		url: '/like_answer/',
		method: 'POST',
		data: {
			id: $btn.data('id'),
			type: $btn.data('type'),
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
		}
	}).done(function(resp) {
		if(resp && resp.status == 'ok') 
		{
			window.location.reload();
		}
	})
	return false;
});
