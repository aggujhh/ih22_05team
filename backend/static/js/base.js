console.log("base.js");


$(document).ready(function() {
    // サイドメニューの表示とナビボタン非表示
    $('.nav-button').on('click',function() {
        $('.sidebar').toggleClass('show');
        $('.nav-button').toggle();
    });

    // サイドメニューの非表示とnavボタンの表示
    $('.close-button').on('click',function() {
        $('.sidebar').removeClass('show');
        $('.nav-button').toggle();
    });
});