        $('#chatBotMainContainer').animate({
            scrollTop: $('#chatBotMainContainer')[0].scrollHeight
        }, "slow");




        $(".floating-chat ").click(function () {


            $(".bottom.close").addClass('open');

        });


        $(".bottom.close").click(function () {



            $(this).removeClass('open');

        });


        $(".mic-button").click(function () {

            $(this).toggleClass('recording');


        });




        $(".bottom.close").click(function () {

            $('.floating-chat').find('.chat').removeClass('enter').hide();

            $('.floating-chat').removeClass('expand');

            setTimeout(function () {
                $('.floating-chat').find('.chat').removeClass('enter').show()
                $('.floating-chat').click(openElement);
            }, 100);

        });




        $("#chatInput").on('change keydown paste input', function () {


            $(".mic-button").fadeOut();

        });




        //            $('#chatInput').focusout(function() {
        //                if ($(this).val().length < 1) {
        //
        //                    $(".mic-button").fadeIn();
        //
        //                }
        //            });

        //            $('#chatInput').on("change keyup paste", function() {
        //                     
        //                    alert("sada");
        //                    
        //                    $(".mic-button").fadeOut();
        // 
        //                    
        //                    if ($(this).val().length < 1) {
        //
        //                    $(".mic-button").fadeOut();
        //
        //                    }
        //            });





        //            $('#chatInput').keypress(function()
        //                {
        //                    
        //                if( $(this).val().length === 0 ) {
        //                        
        //                     $(".speak-logo").fadeIn();   
        //                         
        //                }
        //                
        //                else{
        //                   $(".speak-logo").fadeOut();   
        //                }
        //                
        //            });
        //            





        $(document).ready(function () {

            $(".icon-down").click(function () {
               

                $(this).closest(".from-them").toggleClass('downloading');
              

            });

            //            $('.variable-width').slick({
            //            dots: false,
            //            infinite: false,
            //            speed: 300,
            //            slidesToShow: 1,
            //            variableWidth: true
            //        });
            // 


            //                $("#chatInput").keypress(function (e) {
            //                    $('#chatBotMainContainer').animate({
            //                        scrollTop: $('#chatBotMainContainer')[0].scrollHeight
            //                    }, "slow");
            //                });
            //
            //                $("#chatInput").on('change keydown paste input', function () {
            //                    $('#chatBotMainContainer').animate({
            //                        scrollTop: $('#chatBotMainContainer')[0].scrollHeight
            //                    }, "slow");
            //                });


            $("#chatInput").focus(function () {
                $('#chatBotMainContainer').animate({
                    scrollTop: $('#chatBotMainContainer')[0].scrollHeight
                }, "slow");


            });

            $('#chatBotMainContainer').animate({
                scrollTop: $('#chatBotMainContainer')[0].scrollHeight
            }, "slow");




        });



        $(document).on('click', '.waves', function (e) {
            if ($(this).hasClass('disabled')) return;

            const offset = $(this).offset();

            const eventX = e.pageX - offset.left;
            const eventY = e.pageY - offset.top;

            const diameter = Math.min(this.offsetHeight, this.offsetWidth, 50);

            const ripple = $('<div/>', {
                class: "wavesWrapper",
                appendTo: $(this)
            });

            $('<div/>', {
                class: "wavesEffect",
                css: {
                    width: diameter,
                    height: diameter,
                    left: eventX - (diameter / 2),
                    top: eventY - (diameter / 2),
                },
                appendTo: ripple,
                one: {
                    animationend: function () {
                        ripple.remove();
                    }
                }
            });
        });
