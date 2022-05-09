class SpeechRecognitionApi {
    constructor(options) {
        const SpeechToText = window.speechRecognition || window.webkitSpeechRecognition;
        this.speechApi = new SpeechToText();
        this.speechApi.continuous = false;
        this.speechApi.lang = 'vi-VN';
        this.speechApi.interimResults = false;
        // this.output = options.output ? options.output : document.createElement('div');
        this.output = options.output;
        // console.log(this.output);
        this.speechApi.onresult = (event) => {
            console.log(event);
            let resultIndex = event.resultIndex;
            let transcript = event.results[resultIndex][0].transcript;
            console.log('transcript>>', transcript);
            // console.log(this.output);
            this.output.value = transcript;
            document.getElementById("sendButton").click();
        }
    }

    init() {
        this.speechApi.start();
    }

    stop() {
        this.speechApi.stop();
    }
}

window.onload = function () {
    var speech = new SpeechRecognitionApi({
        output: document.querySelector('#userInput')
    })

    document.querySelector('#voiceButton').addEventListener('click', function () {
        speech.init()
    })

    // document.querySelector('#voiceButton').addEventListener('click', function () {
    //     speech.stop()
    // })

}