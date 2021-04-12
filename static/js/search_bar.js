$(document).ready(function(){
    $(".default_option").click(function(){
        $(".dropdown ul").toggleClass("active");
    });

    $(".dropdown ul li").click(function(){
        var text = $(this).text();
        $(".default_option").text(text);
        $(".dropdown ul").removeClass("active");
    })
})