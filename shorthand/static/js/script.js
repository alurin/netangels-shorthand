(function($) {
    $(document).ready(function() {
        $('.js-history-back').click(function(e) {
            e.preventDefault();
            e.stopPropagation();
            window.history.go(-1);
        });
    })
})(jQuery);