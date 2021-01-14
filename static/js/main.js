$.fn.digits = function(){ 
    return this.each(function(){ 
        $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") ); 
    })
}
$(".split-number").digits();

//ُMain Slider in index page
var showingSlide;

$('.slide:nth-child(1)').css('z-index', 1);
$('.slide:nth-child(1)').css('opacity', 1);
showingSlide = 1;
slideCount = $('.slide').length;

if (slideCount <= 1)
{
    $(".arrow").hide();
}

$('.next').on('click', function () {
    $('.slide:nth-child(' + showingSlide + ')').css('opacity', 0);
    $('.slide:nth-child(' + showingSlide + ')').css('z-index', '-1');
    if (showingSlide == slideCount)
    {
        showingSlide = 1;
    }
    else {
        showingSlide += 1;
    }
    $('.slide:nth-child(' + showingSlide + ')').css('opacity', 1);
    $('.slide:nth-child(' + showingSlide + ')').css('z-index', 1);
})
$('.prev').on('click', function () {
    $('.slide:nth-child(' + showingSlide + ')').css('opacity', 0);
    $('.slide:nth-child(' + showingSlide + ')').css('z-index', '-1');
    if (showingSlide == 1)
    {
        showingSlide = slideCount;
    }
    else {
        showingSlide -= 1;
    }
    $('.slide:nth-child(' + showingSlide + ')').css('opacity', 1);
    $('.slide:nth-child(' + showingSlide + ')').css('z-index', 1);
})

// Slick Sliders
$(document).ready(function(){
    $('.slider-slick').slick({
        'setting-name': 'setting-value',
        autoplay: true,
        autoplayspeed: 3000,

        // prevArrow: '<i class="far fa-angle-right">',
        // nextArrow: '<i class="far fa-angle-left">',

        dots: false,
        infinite: true,
        speed: 600,
        slidesToShow: 6,
        slidesToScroll: 1,
        responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 1,
                infinite: true,
            }
        },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 1
            }
        },
        {
            breakpoint: 480,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1
            }
        }]
    });
});

$(document).ready(function(){
    $('.slider-slick-single').slick({
        'setting-name': 'setting-value',
        autoplay: true,
        autoplayspeed: 3000,

        // prevArrow: '<i class="far fa-angle-right">',
        // nextArrow: '<i class="far fa-angle-left">',

        dots: false,
        infinite: true,
        speed: 600,
        slidesToShow: 1,
        slidesToScroll: 1,
        // asNavFor: '.slider-slick-gallery',
    });
});

$(document).ready(function(){
    $('.slider-slick-gallery').slick({
        'setting-name': 'setting-value',
        autoplay: true,
        autoplayspeed: 3000,
        asNavFor: '.slider-slick-single',
        focusOnSelect: true,

        // prevArrow: '<i class="far fa-angle-right">',
        // nextArrow: '<i class="far fa-angle-left">',

        dots: false,
        infinite: true,
        speed: 600,
        slidesToShow: 5,
        slidesToScroll: 1,
        responsive: [
        {
            breakpoint: 992,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 1,
                infinite: true,
            }
        },
        {
            breakpoint: 768,
            settings: {
                slidesToShow: 5,
                slidesToScroll: 1,
                infinite: true,
            }
        },
        {
            breakpoint: 576,
            settings: {
                slidesToShow: 5,
                slidesToScroll: 1,
                infinite: true,
            }
        }]
    });
});

// Sidebar Products
// $(".collapse").hide();

// $(".collapse-link").click(function () {
//         $(this).children('.collpase-link-toggle').children('i').toggleClass('open');
//         $(this).children(".collapse").animate({
//             height: 'toggle'
//         }, 500)
// })
!function ($) {
    
    // Le left-menu sign
    /* for older jquery version
    $('#left ul.nav li.parent > a > span.sign').click(function () {
        $(this).find('i:first').toggleClass("icon-minus");
    }); */
    
    $(document).on("click","#left ul.nav li.parent > a > span.sign", function(){          
        $(this).find('i:first').toggleClass("icon-minus");      
    }); 
    
    // Open Le current menu
    $("#left ul.nav li.parent.active > a > span.sign").find('i:first').addClass("icon-minus");
    $("#left ul.nav li.current").parents('ul.children').addClass("in");

}(window.jQuery);



// Hide Usermenu in Header
$(document).mouseup(function(e) 
{
    var container = $(".user-menu");

    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(e.target) && container.has(e.target).length === 0) 
    {
        container.hide();
    }
});

// Show usermenu in Header
$(".logged-in").click(function () {
    $(".user-menu").toggle();
})

// $('form').on('focus', 'input[type=number]', function (e) {
//     $(this).on('wheel.disableScroll', function (e) {
//       e.preventDefault()
//     })
// })
// $('form').on('blur', 'input[type=number]', function (e) {
//     $(this).off('wheel.disableScroll')
// })

//When Pay Button Clicked "sweetalert2"
$("#pay-btn").click(function () {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-success ml-3',
          cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
      })
      
      swalWithBootstrapButtons.fire({
        title: 'وضعیت پرداخت',
        text: "پرداخت موفقیت آمیز بود؟",
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'بله',
        cancelButtonText: 'خیر',
        reverseButtons: false
      }).then((result) => {
        if (result.isConfirmed) {
          swalWithBootstrapButtons.fire({
            title: 'موفق',
            text: 'سفارش با موفقیت ثبت شد',
            icon: 'success',
            confirmButtonText: 'باشه',
          })
        } else if (
          /* Read more about handling dismissals below */
          result.dismiss === Swal.DismissReason.cancel
        ) {
          swalWithBootstrapButtons.fire({
            title: 'نا موفق',
            text: 'پرداخت با مشکل مواجه شد!',
            icon: 'error',
            confirmButtonText: 'باشه',
            })
        }
      })
})

//Submit Comment "sweetalert2"
$(document).on('click' ,".send-comment", function () {
    Swal.fire({
        icon: 'success',
        title: 'ثبت نظر',
        text: 'نظر شما با موفقیت ثبت گردید',
      })
})

//Make Reply Form in Comments
$(".reply-btn").click(function (e) {
    e.preventDefault();
    $(".reply-form").remove();
    var whichComment = $(this).attr('val');
    // console.log('which comment? answer:', whichComment);

    $(".comment[val='" + whichComment + "'").append(
    '<div class="reply-form">' +
        '<textarea name="comment" id="product-comment" class="form-control" cols="20" rows="7" placeholder="پاسخ خود را اینجا بنویسید..."></textarea>' +
        '<div class="send-comment-btn text-left mt-3">' +
            '<button class="btn btn-primary send-comment">ارسال</button>' +
        '</div>' +
    '</div>')
})

// Product Rate in Product Page
$(".product-rate input").on('change', function () {
    var ProductRate;
    
    if ($("#check-1").prop("checked"))
    {
        ProductRate = 1;
    }
    else if ($("#check-2").prop("checked"))
    {
        ProductRate = 2;
    }
    else if ($("#check-3").prop("checked"))
    {
        ProductRate = 3;
    }
    else if ($("#check-4").prop("checked"))
    {
        ProductRate = 4;
    }
    else if ($("#check-5").prop("checked"))
    {
        ProductRate = 5;
    }

})
$(".post-rate input").on('change', function () {
    var PostRate;
    
    if ($("#check-1").prop("checked"))
    {
        PostRate = 1;
    }
    else if ($("#check-2").prop("checked"))
    {
        PostRate = 2;
    }
    else if ($("#check-3").prop("checked"))
    {
        PostRate = 3;
    }
    else if ($("#check-4").prop("checked"))
    {
        PostRate = 4;
    }
    else if ($("#check-5").prop("checked"))
    {
        PostRate = 5;
    }
})

//Edit information
$("#edit-information").click(function () {
    $(".information-card-content fieldset").prop('disabled', false);
    $(this).hide();
    $("#save-information").show();
})

$("#save-information").click(function (){
    $(".information-card-content fieldset").prop('disabled', true);
    $(this).hide();
    $("#edit-information").show();
})


var minPrice = 0;
var maxPrice = 51000000;

$( function() {
    $( "#filter-price-range" ).slider({
      range: true,
      min: 0,
      max: 51000000,
      values: [ 0, 51000000 ],
      slide: function( event, ui ) {
        minPrice = ui.values[0];
        maxPrice = ui.values[1];
        $( "#amount" ).val( ui.values[ 1 ].toLocaleString() + " تومان" + " - " + ui.values[ 0 ].toLocaleString() + " تومان" );
      }
    });
    $( "#amount" ).val($( "#filter-price-range" ).slider( "values", 1 ).toLocaleString() +
    " تومان" +
    " - " + $( "#filter-price-range" ).slider( "values", 0 ).toLocaleString() +
    " تومان");
  } );

  $(".product-color-selection-item").click(function () {
    $(".product-color-selection-item").removeClass('active');
    $(this).addClass('active');
  })