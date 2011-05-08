function set_mouse_over(id, off_img, on_img, target) {
    var element = $('#' + id);
    if (element.attr("src").indexOf("_on") >= 0)
        return;
    element.hover(
            function () {
                var src = on_img ? on_img : $(this).attr("src").match(/[^\.]+/) + "_on.jpg";
                var t = target ? $('#' + target) : $(this)
                t.attr("src", src);
            },
            function () {
                var src = off_img ? off_img : $(this).attr("src").replace("_on", "");
                var t = target ? $('#' + target) : $(this)
                t.attr("src", src);
            });
}
var a = $('<img />').attr('src', '/media/images/logo_phrase_on.jpg');
var b = $('<img />').attr('src', '/media/images/about_kiggle_on.jpg');
var c = $('<img />').attr('src', '/media/images/products_on.jpg');
var d = $('<img />').attr('src', '/media/images/contact_us_on.jpg');
var b = $('<img />').attr('src', '/media/images/tv_teether_remote.jpg');
var c = $('<img />').attr('src', '/media/images/my_1st_mouse_pad.jpg');
var d = $('<img />').attr('src', '/media/images/my_1st_smart_phone.jpg');
set_mouse_over('logo', '/media/images/logo_phrase.jpg', '/media/images/logo_phrase_on.jpg', 'logo_phrase');
set_mouse_over('logo_phrase');
set_mouse_over('about_kiggle');
set_mouse_over('products');
set_mouse_over('contact_us');
set_mouse_over('tv_teether_remote');
set_mouse_over('my_1st_mouse_pad');
set_mouse_over('my_1st_smart_phone');
