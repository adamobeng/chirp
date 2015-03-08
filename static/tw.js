//window.twttr=(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],t=window.twttr||{};if(d.getElementById(id))return;js=d.createElement(s);js.id=id;js.src="https://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);t._e=[];t.ready=function(f){t._e.push(f);};return t;}(document,"script","twitter-wjs"));

function textchange(e) {
	$('#twitter').attr({href: 'https://twitter.com/share?url=tw&text=' + encodeURIComponent($(this).val())});
	// http://stackoverflow.com/a/2848483
	length = $(this).val().length;
	$('#length').text(140-length);
}
jQuery(document).ready(function($) {
	$('#text').spellcheck({events: 'keyup', url: '/spellcheck.php'});
	$('#text').change(textchange);
	$('#text').keyup(textchange);
});
