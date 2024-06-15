a
let $sessionId = '';
let suggestions;
let pledges;
let branches;
var element = $('.floating-chat');
let chartStarted = false;

let metaData = {
    platform_name: '',
    platform_version: '',
    platform_layout: '',
    platform_product: '',
    platform_manufacturer: '',
    platform_os: '',
    platform_description: '',
    latitude: 0,
    longitude: 0,
    accuracy : 0,
    ipv4: '',
    ipv6: ''
};


$(document).ready(function () {

    console.log("Starting document ready @ " + new Date())


    window.addEventListener("message", receiveMessage, false);

    getPublicIP();

    console.log("After getPublicIP @ " + new Date())
    setTimeout(function () {
        element.addClass('enter');
    }, 1000);

    metaData.platform_name = platform.name;
    metaData.platform_version = platform.version;
    metaData.platform_layout = platform.layout;
    metaData.platform_product = platform.product;
    metaData.platform_manufacturer = platform.manufacturer;
    metaData.platform_os = platform.os;
    metaData.platform_description = platform.description;

    element.click(openElement);
    getLocation();
    setSession();

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
            //var audio = new Audio("static/js/question.wav");
            //audio.play();

            // Trigger the button element with a click
            submitChat();

            $(".mic-button").fadeIn();
            $('#chatBotMainContainer').animate({
                scrollTop: $('#chatBotMainContainer')[0].scrollHeight
            }, "slow");


        }
    });

    console.log("Ending document ready @ " + new Date())

});


function getLocation() {

    console.log('Calling getLocation');
    parent.postMessage("location", "*");
    console.log("After getLocation - latitude = " + metaData.latitude + ", longitude = " + metaData.longitude)
}


function receiveMessage(event) {

    let eventData = event.data.split(":");
    console.log("eventData[0] = " + eventData[0]);
    console.log("eventData[1] = " + eventData[1]);

    if (eventData[0] == "mcs") {
        $sessionId = eventData[1];

    } else if (eventData[0] == "location") {
        console.log(eventData[1])
        let locValues = eventData[1].split(",");
        metaData.latitude = Number(locValues[0]);
        metaData.longitude = Number(locValues[1]);
        metaData.accuracy = Number(locValues[2]);

    } else {
        if (eventData[1] == undefined) {
            $sessionId = eventData[0];
        }
    }
}

function getPublicIP() {

    let responseText = '';
    suggestions = [];
    $.ajax({
        type: "GET",
        data: {},
        async: false,
        crossDomain: true,
        url: "https://api.ipify.org?format=json",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (response) {
            metaData.ipv4 = response.ip;
        }
    });
}


function openElement() {

    parent.postMessage("open", "*");

    if (chartStarted == false)
        initiateChat();

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
    parent.postMessage("close", "*");

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

function submitChat() {

    const inputText = document.getElementById("chatInput").value;

    if ($.trim(inputText) != "") {
        var audio = new Audio("static/js/question.wav");
        audio.play();
        $("#chatOptions").remove();

        const inputHtml = createInputTextHtml(inputText);
        document.getElementById("chatBotMainContainer").innerHTML += inputHtml;

        const progressHtml = createProgressHtml();
        document.getElementById("chatBotMainContainer").innerHTML += progressHtml;

        document.getElementById("chatInput").value = "";

        const responseText = processInput(inputText);
    }
}

function initiateChat() {
    var audio = new Audio("static/js/start.wav");
    audio.play();
    processInput("VGFrZSBtZSBob21l");
}

function setSession() {

    if ($sessionId == '') {
        parent.postMessage("mcs", "*");
    }
    console.log('$sessionId = ' + $sessionId);
}

function processInput(inputText) {

    console.log("Inside processInput @ " + new Date())

    setSession();

    if (metaData.latitude == 0 || metaData.longitude == 0)
        getLocation();

    console.log("Inside processInput - latitude = " + metaData.latitude + ", longitude = " + metaData.longitude)

    let responseText = '';
    suggestions = [];
    // const serverURL = "https://chat.manappuram.com/api/processInput";
//	const serverURL = "http://127.0.0.1:5000/api/processInput";
	const serverURL = "http://127.0.0.1:5000/api/processInput";
    // alert(serverURL)

    chartStarted = true;

    $.ajax({
        type: "GET",
        // url: "https://chat.manappuram.com:8080/chatbotapi/api/",
        url: serverURL,
        dataType: "json",
        contentType: "application/x-www-form-urlencoded",
        cache: false,
        data: {
            'inputData': inputText,
            'sessionid': $sessionId,
            'metaData': JSON.stringify(metaData, null, 2),
        },
    }).done(function (response) {
        var audio = new Audio("static/js/answer.wav");
        audio.play();
        console.log("Inside processInput success @ " + new Date())
        console.log(response)
        responseText = response.responseText;
        suggestions = response.suggestions;
        branches = response.branches;
        pledges = response.pledges;
        $("#typing").remove();

        const responseHtml = createResponseTextHtml(responseText);
        document.getElementById("chatBotMainContainer").innerHTML += responseHtml;

        if (suggestions.length > 0) {
            const suggestionHtml = createSuggestionHtml(suggestions);
            document.getElementById("chatBotMainContainer").innerHTML += suggestionHtml;
        }

        if (pledges.length > 0) {

            const pledgesHtml = createPledgesHtml(pledges);
            document.getElementById("chatBotMainContainer").innerHTML += pledgesHtml;
        }

        if (branches.length > 0) {

            if (metaData.latitude == 0 || metaData.longitude == 0) {

                const responseText = "Your location not available at the moment. Please enable location service in your device and allow the browser to use the service. Please try again. "
                const responseHtml = createResponseTextHtml(responseText);
                document.getElementById("chatBotMainContainer").innerHTML += responseHtml;
            } else {
                const branchesHtml = createBranchesHtml(branches);
                document.getElementById("chatBotMainContainer").innerHTML += branchesHtml;

                if (metaData.accuracy > 100){
                    const responseText = "Did you think the detected location isn't correct?. That means, there are no location source with high accuracy available in your current device or network. This is likely happen if you use Laptop / PC with WiFi or Cable LAN Connection. "
                    const responseHtml = createResponseTextHtml(responseText);
                    document.getElementById("chatBotMainContainer").innerHTML += responseHtml;
                }

            }

        }

        var swiper = new Swiper('.swiper-container', {
            slidesPerView: 'auto',
            spaceBetween: 10,
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });

        $('#chatBotMainContainer').animate({
            scrollTop: $('#chatBotMainContainer')[0].scrollHeight
        }, "slow");

        $("#chatInput").focus();

        console.log("Finishing processInput @ " + new Date())
    }).fail(function (jqXHR, textStatus, errorThrown) {
        // If fail
        console.log(textStatus + ': ' + errorThrown);
        $("#typing").remove();
        const responseTextHtml = createResponseTextHtml("Sorry! I didn't get it. Please try again.");
        document.getElementById("chatBotMainContainer").innerHTML += responseTextHtml;
        $('#chatBotMainContainer').animate({
            scrollTop: $('#chatBotMainContainer')[0].scrollHeight
        }, "slow");

        $("#chatInput").focus();
    });


    return responseText;
}

function changeLanguage() {
    //var audio = new Audio("static/js/question.wav");
    //        audio.play();
	callToAction("Change Language");
}

function resetHome() {
//var audio = new Audio("static/js/question.wav");
//            audio.play();
    getLocation();
    callToAction("VGFrZSBtZSBob21l", false);
}

//function resetHome1() {
//    callToAction("voiceOptionSelectedVOS", false);
//}


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

    let suggestionHtml = '<div id="chatOptions" class="">';

    for (let suggestion of suggestions) {
        // console.log('suggestion = ', suggestion)
        suggestionHtml += '<button class="option " onclick="javascript:callToAction(' +
            "'" + suggestion.suggestionInput + "'" +
            ')" style="">' +
            suggestion.suggestionText + '</button>';
    }
    suggestionHtml += '</div>';

    return suggestionHtml;
}

function createPledgesHtml(pledges) {

    let pledgesHtml = '<div id="PledgeDiv" class="chat-message message-came card-ele carousel new bot-message"><span class="from-icon"></span>';
    pledgesHtml += '<div class="swiper-container"><div class="swiper-wrapper">';

    for (let pledge of pledges) {

        pledgesHtml += '<div class="swiper-slide"><div class="card"><div class="card_details"><div class="card_title">\n'
        pledgesHtml += '<strong>Pledge Number - </strong>'+ pledge.pledgeCd
        pledgesHtml += '</div><div class="card_description"><strong>Loan Amount</strong><br>'
        pledgesHtml += pledge.totalAmount + '<br><br>'
        pledgesHtml += '<strong>Due Date</strong><br>'
        pledgesHtml += pledge.dueDate + '<br><br>'
        pledgesHtml += '<strong>Renewal Date</strong><br>'
        pledgesHtml += pledge.renewalDate
        pledgesHtml += '</div><div class="card_buttons"><button style="text-align:left" tabindex="0" title="'
        pledgesHtml += pledge.action
        pledgesHtml += '"><a href="#" onclick="">'
        pledgesHtml += pledge.action
        pledgesHtml += '</a></button>'

        pledgesHtml += '</div></div></div></div>'

    }
    pledgesHtml += '</div><!-- Add Pagination --><div class="swiper-pagination"></div></div></div> ';

    return pledgesHtml;
}

function createBranchesHtml(branches) {

    let branchesHtml = '<div id="branchDiv" class="chat-message message-came card-ele carousel new bot-message"><span class="from-icon"></span>';
    branchesHtml += '<div class="swiper-container"><div class="swiper-wrapper">';

    for (let branch of branches) {

        branchesHtml += '<div class="swiper-slide"><div class="card"><div class="card_details"><div class="card_title">\n'
        branchesHtml += branch.branchCd + ' - ' + branch.branchName
        branchesHtml += '</div><div class="card_description"><strong>Address</strong><br>'
        branchesHtml += branch.address + '<br><br>'
        branchesHtml += '<strong>MobileNo</strong><br>'
        branchesHtml += branch.phone
        branchesHtml += '</div><div class="card_buttons"><button style="text-align:left" tabindex="0" title="'
        branchesHtml += branch.action
        branchesHtml += '"><a href="#" onclick="performBranchAction(\'' + branch.action + '\',\'' + branch.branchCd + '\',\'' + branch.branchName + '\')">'
        branchesHtml += branch.action
        branchesHtml += '</a></button>'
        branchesHtml += '</div></div></div></div>'

    }
    branchesHtml += '</div><!-- Add Pagination --><div class="swiper-pagination"></div></div></div> ';

    return branchesHtml;
}

function performBranchAction(action, branchCd, branchName) {

    // alert('action = ' + action + 'branchCd = ' + branchCd + ' branchName = ' + branchName)
    if (action == 'Select Branch') {
        callToAction(branchCd, false);
        $("#branchDiv").remove();
    }
}

function createProgressHtml() {

    let progressHtml = '<div class="typingdiv" id="typing" style="/* display:none; */"> ' +
        '<span class="dot"></span> ' +
        '<span class="dot"></span> ' +
        '<span class="dot"></span> ' +
        '</div> ';
    return progressHtml;
}

function callToAction(inputText, showInput = true) {
    $("#chatOptions").remove();

    if (showInput == true) {
        const inputHtml = createInputTextHtml(inputText);
        document.getElementById("chatBotMainContainer").innerHTML += inputHtml;
    }
//    if(inputText == 'voiceOptionSelectedVOS'){
////    const progressHtml = createProgressHtml();
////    document.getElementById("chatBotMainContainer").innerHTML += progressHtml;
//
//    document.getElementById("chatInput").value = "";
//
//    processInput(inputText);
//    }else{

    const progressHtml = createProgressHtml();
    document.getElementById("chatBotMainContainer").innerHTML += progressHtml;

    $('#chatBotMainContainer').animate({
        scrollTop: $('#chatBotMainContainer')[0].scrollHeight
    }, "slow");

    document.getElementById("chatInput").value = "";
    var audio = new Audio("static/js/question.wav");
    audio.play();
    processInput(inputText);
//}
}


// function create_UUID() {
//     var dt = new Date().getTime();
//     var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
//         var r = (dt + Math.random() * 16) % 16 | 0;
//         dt = Math.floor(dt / 16);
//         return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
//     });
//     return uuid;
// }
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
    // console.log(timeFormatted);
    return timeFormatted;
}

//function startDictation() {
//
//    if (window.hasOwnProperty('webkitSpeechRecognition')) {
//        var recognition = new webkitSpeechRecognition();
//
//
//
////        recognition.continuous = false;
////        recognition.interimResults = flase;
//        recognition.lang = "en-US";
//
//
//        recognition.onresult = function(event) {
//            document.getElementById("chatInput").value = event.results[0][0].transcript;
//
//        }
//        recognition.onerror = function(event) {
//            document.getElementById("chatInput").value = "data not found"
//
//            console.error(event);
//
//        }
//        recognition.start();
//    }
//
//}





