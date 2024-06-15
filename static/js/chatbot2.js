let $sessionId = '';
let suggestions;
var element = $('.floating-chat');
let latitude = 0;
let longitude = 0;


$(document).ready(function () {

    setTimeout(function () {
        element.addClass('enter');
    }, 1000);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    }

    element.click(openElement);

    initiateChat();

    // Get the input field
    const input = document.getElementById("chatInput");

    // Execute a function when the user releases a key on the keyboard
    $(".action-btn .send-button").click(function () {

        // Trigger the button element with a click
        submitChat();

        $(".mic-button").fadeIn();

        $('#chatBotMainContainer').animate({
            scrollTop: $('#chatBotMainContainer')[0].scrollHeight
        }, "slow");
        
        
        

    });

    // Execute a function when the user releases a key on the keyboard
    input.addEventListener("keyup", function (event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            // Cancel the default action, if needed
            event.preventDefault();

            // Trigger the button element with a click
            submitChat();

            $(".mic-button").fadeIn();
            $('#chatBotMainContainer').animate({
                scrollTop: $('#chatBotMainContainer')[0].scrollHeight
            }, "slow");
            
            
        }
    });


});

function openElement() {
    var messages = element.find('.messages');
    var textInput = element.find('.text-box');
    element.find('>i').hide();
    element.addClass('expand');
    element.find('.chat').addClass('enter');
    var strLength = textInput.val().length * 2;
    // textInput.keydown(onMetaAndEnter).prop("disabled", false).focus();
    element.off('click', openElement);
    element.find('.header button').click(closeElement);
    // element.find('#sendMessage').click(sendNewMessage);
    messages.scrollTop(messages.prop("scrollHeight"));
}

function closeElement() {
    element.find('.chat').removeClass('enter').hide();
    element.find('>i').show();
    element.removeClass('expand');
    element.find('.header button').off('click', closeElement);
    // element.find('#sendMessage').off('click', sendNewMessage);
    // element.find('.text-box').off('keydown', onMetaAndEnter).prop("disabled", true).blur();
    setTimeout(function () {
        element.find('.chat').removeClass('enter').show()
        element.click(openElement);
    }, 500);
}

function showPosition(position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
}

function submitChat() {
    $("#chatOptions").remove();
    const inputText = document.getElementById("chatInput").value;
    const inputHtml = createInputTextHtml(inputText);
    document.getElementById("chatBotMainContainer").innerHTML += inputHtml;
    document.getElementById("chatInput").value = "";

    const responseText = processInput(inputText);
    const responseHtml = createResponseTextHtml(responseText);
    document.getElementById("chatBotMainContainer").innerHTML += responseHtml;

    if (suggestions.length > 0) {
        const suggestionHtml = createSuggestionHtml(suggestions);
        document.getElementById("chatBotMainContainer").innerHTML += suggestionHtml;
    }

}

function initiateChat() {
    $sessionId = create_UUID();

    const responseText = processInput("Hi");
    const responseHtml = createResponseTextHtml(responseText);
    document.getElementById("chatBotMainContainer").innerHTML += responseHtml;

    if (suggestions.length > 0) {
        const suggestionHtml = createSuggestionHtml(suggestions);
        document.getElementById("chatBotMainContainer").innerHTML += suggestionHtml;
    }

}


function processInput(inputText) {

    let responseText = '';
    suggestions = [];
    $.ajax({
        type: "GET",
        data: {
            'inputData': inputText,
            'sessionId': $sessionId,
            'latitude': latitude,
            'longitude': longitude
        },
        async: false,
        crossDomain: true,
        // url: "http://localhost:8920/dashboard/api/processInput",
        url: "http://127.0.0.1:5000/api/processInput",
        // url: "https://ba.manappuram.com/chatbotapi/api/processInput",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (response) {
            responseText = response.responseText;
            suggestions = response.suggestions;
            console.log('suggestions = ', suggestions)
        }
    });

    return responseText;
}

function create_UUID() {
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (dt + Math.random() * 16) % 16 | 0;
        dt = Math.floor(dt / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

function createInputTextHtml(inputText) {

    let inputHtml =
        '<div class="chat-message from-me message-came new first">' +
        '<div>' + inputText + '</div> ' +
        '</div> ' +
        '<div class="clearfix"> ' +
        '</div> ' +
        '<div class="timestamp-user "> ' + timeFormatter() + '<i class="fa fa-fw 1585844009677 fa-check" style="font-size: 12px"></i> ' +
        '</div>';

    return inputHtml;
}

function createResponseTextHtml(responseText) {

    let responseHtml =
        '<div id="chatBotMain" class="row"> ' +
        '<div class="chat-message message-came quick-reply from-them bot-message  new first"> ' +
        '<span class="from-icon" src="images/mf-logo.jpg"></span> ' +
        '<div>' + responseText + '</div> ' +
        '</div> ' +
        '<div class="clearfix"> </div>' +
        '<div class="timestamp-bot">' + timeFormatter() + '</div> ' +
        '</div>';

    return responseHtml;
    
    $('.variable-width').slick({
                dots: false,
                infinite: false,
                speed: 300,
                slidesToShow: 1,
                variableWidth: true
            });
}

function createSuggestionHtml(suggestions) {

    let responseHtml = '<div id="chatOptions" class="">';

    for (let suggestion of suggestions) {
        console.log('suggestion = ', suggestion)
        responseHtml += '<button class="option " onclick="javascript:callToAction(' +
            "'" + suggestion.suggestionInput + "'" +
            ')" style="">' +
            suggestion.suggestionText + '</button>';
    }
    responseHtml += '</div>';

    return responseHtml;
}

function callToAction(inputText) {
    $("#chatOptions").remove();

    const inputHtml = createInputTextHtml(inputText);
    document.getElementById("chatBotMainContainer").innerHTML += inputHtml;
    document.getElementById("chatInput").value = "";

    const responseText = processInput(inputText);
    const responseHtml = createResponseTextHtml(responseText);
    document.getElementById("chatBotMainContainer").innerHTML += responseHtml;
}

function timeFormatter() {

    let weekday = new Array(7);
    weekday[0] = "Sun";
    weekday[1] = "Mon";
    weekday[2] = "Tue";
    weekday[3] = "Wed";
    weekday[4] = "Thu";
    weekday[5] = "Fri";
    weekday[6] = "Sat";

    const currentDate = new Date();
    let hour, amPm;

    if (currentDate.getHours() >= 12) {
        hour = parseInt(currentDate.getHours()) - 12;
        amPm = "PM";
    } else {
        hour = currentDate.getHours();
        amPm = "AM";
    }
    const timeFormatted = weekday[currentDate.getDay()] + " " + hour + ":" + currentDate.getMinutes() + " " + amPm;
    console.log(timeFormatted);
    return timeFormatted;
}
