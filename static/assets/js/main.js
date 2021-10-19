$(function() {

    $(window).on('load', function(){
        $('.loader-container').fadeOut(1000);
    });


    $('.list').click(function(){
        const value = $(this).attr('data-filter');
        if (value=='all') {
            $('.abc').show('1000');
        } else {
            $('.abc').not('.'+value).hide('1000');
            $('.abc').filter('.'+value).show('1000');
        }
    });


    $('.owl-carousel').owlCarousel({
        dots: false,
        loop: true,
        margin: 10,
        stagePadding: 0,
        nav: true,
        autoplay: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        responsive:{
            0:{
                items:2
            },
            600:{
                items:2.5
            },
            800:{
                items:2.1
            },
            1000:{
                items:3.5
            }
        }
    });


    $('#arrival').prop("disabled", true);
    $('#one').prop("checked", true);

    $('input[name=trip').click(function(){
        if ($('#two').is(':checked')) {
            $('#arrival').prop('disabled', false)
        }
        else {
            $('#arrival').prop('disabled', true)
        }
    });

    var mindate = new Date();
    $("#departure").datepicker({
        showAnim: 'slide',
        numberOfMonth: 2,
        dateFormat: 'yy-mm-dd',
        minDate: mindate,
        onClose: function (selectedDate) {
            $('#arrival').datepicker("option","minDate", selectedDate);
        }
    });

    $("#arrival").datepicker({
        showAnim: 'slide',
        numberOfMonth: 1,
        dateFormat: 'yy-mm-dd',
        minDate: mindate,
        onClose: function (selectedDate) {
            $('#arrival').datepicker("option","minDate", selectedDate);
        }
    });


    $('#filterSlide1').css('display', 'none');
    $('#filterSlide2').css('display', 'none')
    $('#searchCollapse').click(function(){
        $('#filterSlide1').slideToggle();
        $('#filterSlide2').slideToggle();
    });

    $('.phoneNumber').keyup(function() {
        var check = document.getElementsByClassName('phoneNumber').val();
        if (isNumeric(check)) {
            console.log(check);
        }
        else{
            alert(check + "is not a phone number");
        }
    });

    
});

    function selection(){

        var seats = document.getElementsByName('seatSelection');
        var seatNumber = document.getElementsByClassName('seatNumber');
        var seatChecked = 0;
        var count;
        var check=0;
        var list = new Array;
        var totalPassengers = document.getElementById('totalPassengers').value;

        for(count=0; count<seats.length; count++){
            if(seats[count].checked==true){
                list.push(seats[count].id)
                seatChecked = seatChecked + 1;

                if(seatChecked>totalPassengers){
                    alert('Please Unchecked Previous Seat');
                    return false;      
                }
                else{
                    if(check<seatNumber.length){
                        document.getElementById('seat_result').innerHTML = list.join(",");
                        seatNumber[check].value = seats[count].id;
                        check++;
                    }
                }
            }
        }  
    }

    function logoutPopup(){
        swal({
            title: "Are you sure?",
            text: "You Want To Logout.",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((willDelete) => {
            if (willDelete) {
            swal("Logout successfull!!!", {
            icon: "success",
            });
        }
    });

}
