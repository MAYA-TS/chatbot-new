<script type="text/javascript"> (function () 
    {

    let latitude = 0;
    let longitude = 0;
    let accuracy = '';

    const options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };

    function create_UUID() {
        var dt = new Date().getTime();
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = (dt + Math.random() * 16) % 16 | 0;
            dt = Math.floor(dt / 16);
            return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
        return uuid;
    }

    function getPosition(position) {
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;
        accuracy = position.coords.accuracy;
    }

    function errorCallback(error) {
        console.log("Location errorCallback code = " + error.code);
    }

    function receiveMessage(event) {
        console.log("Received data:", event.data);
        // if (event.origin !== "https://chat.manappuram.com") {
        if (event.origin !=="http://127.0.0.1:5000")
            return;
        }

        const chatDiv = document.getElementById('chat-widget-container');

        if (chatDiv != null && event.data == 'open') {
            const smallScreen = window.matchMedia('(max-width: 768px)').matches;
            if (smallScreen == true) {
                chatDiv.style.width = '100%';
                chatDiv.style.height = '100%';
                chatDiv.style.top = '0';
                chatDiv.style.right = '0';

            } else {
                chatDiv.style.width = '380px';
                chatDiv.style.height = '600px';
            }

        } else if (chatDiv != null && event.data == 'close') {
            chatDiv.style.width = '160px';
            chatDiv.style.height = '60px';
            chatDiv.style.top = '';
            chatDiv.style.right = '20px';
        }

        if (event.data == 'mcs') {
            let mcs = localStorage.getItem("mcs");
            if (mcs == null) {
                mcs = create_UUID();
                localStorage.setItem("mcs", mcs);
            }
            event.source.postMessage("mcs:" + mcs, event.origin);
        }

        if (event.data == 'location') {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(getPosition, errorCallback, options);
            }
            let location = latitude + "," + longitude + "," + accuracy;

            event.source.postMessage("location:" + location, event.origin);

        }
    }

    window.addEventListener("message", receiveMessage, false);
    let mChat = document.createElement('div');
    // mChat.innerHTML = '<div id="chat-widget-container" style="opacity: 1; visibility: visible; z-index: 2147483639; position: fixed; bottom: 10px; width: 160px; height: 60px; max-width: 100%; max-height: calc(100% - 0px); min-height: 0px; min-width: 0px; background-color: transparent; border: 0px; overflow: hidden; right: 20px; transition: none 0s ease 0s !important;"> <iframe src="https://chat.manappuram.com/" allowtransparency="true" allow="autoplay" id="chat-widget" name="chat-widget" scrolling="no" role="application" aria-label="LiveChat chat widget" style="width: 100%; height: 100%; min-height: 0px; min-width: 0px; margin: 0px; padding: 0px; background-image: none; background-position: 0% 0%; background-size: initial; background-attachment: scroll; background-origin: initial; background-clip: initial; background-color: rgba(0, 0, 0, 0); border-width: 0px; float: none; position: absolute; top: 0px; left: 0px; bottom: 0px; right: 0px; transition: none 0s ease 0s !important;"></iframe> </div>';
    mChat.innerHTML = '<div id="chat-widget-container" style="opacity: 1; visibility: visible; z-index: 2147483639; position: fixed; bottom: 10px; width: 160px; height: 60px; max-width: 100%; max-height: calc(100% - 0px); min-height: 0px; min-width: 0px; background-color: transparent; border: 0px; overflow: hidden; right: 20px; transition: none 0s ease 0s !important;"> <iframe src="http://127.0.0.1:5000/" allowtransparency="true" allow="autoplay" id="chat-widget" name="chat-widget" scrolling="no" role="application" aria-label="LiveChat chat widget" style="width: 100%; height: 100%; min-height: 0px; min-width: 0px; margin: 0px; padding: 0px; background-image: none; background-position: 0% 0%; background-size: initial; background-attachment: scroll; background-origin: initial; background-clip: initial; background-color: rgba(0, 0, 0, 0); border-width: 0px; float: none; position: absolute; top: 0px; left: 0px; bottom: 0px; right: 0px; transition: none 0s ease 0s !important;"></iframe> </div>';
    document.body.appendChild(mChat);
})(); </script>
