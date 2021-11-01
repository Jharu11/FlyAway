var closeForm = document.querySelector('.login-modal');

// close login while clicking outside form

        
document.onclick = function(e) {
    if (e.target == closeForm) {
        $('.login-modal').removeClass('active');
    }
}


$(function(){
    // Owl cursol for main slider
    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:10,
        nav:false,
        autoplay: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        responsive:{
            0:{
                items:3.5
            },
            600:{
                items:2.5
            },
            1000:{
                items:3.5
            }
        }
    })

    


    // disable onload propibute of round trip options
    $('#one').prop('checked', true);
    $('#arrival').prop('disabled', true);

    
    // $('#two').click(function(){
    //     $('#arrival').prop('disabled', true);
    // });

    $('#one').click(function(){
        $('#arrival').prop('disabled', true);
    });


    
    $('#sortBy').niceSelect();
    $('.title').niceSelect();

    $('.btn-expand').click(function(){
        $('.sliding').slideToggle();
    });

    




    

});