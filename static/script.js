
(function ($) {
	'use strict';

	$(window).scroll(function () {
		if ($('.navigation').offset().top > 100) {
			$('.navigation').addClass('fixed-nav');
		} else {
			$('.navigation').removeClass('fixed-nav');
		}
	});

})(jQuery);