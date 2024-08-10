class SpeechToText {
    constructor() {
      window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      this.recognition = new window.SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = 'en-US';
  
      this.recognition.onresult = this.handleResult.bind(this);
      this.recognition.onerror = this.handleError.bind(this);
      this.recognition.onend = this.handleEnd.bind(this);
  
      this.finalTranscript = '';
      this.isListening = false;
    }
  
    start() {
      if (!this.isListening) {
        this.recognition.start();
        this.isListening = true;
        console.log("Speech recognition started");
      }
    }
  
    stop() {
      if (this.isListening) {
        this.recognition.stop();
        this.isListening = false;
        console.log("Speech recognition stopped");
      }
    }
  
    handleResult(event) {
      let interimTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          this.finalTranscript += transcript + ' ';
          this.sendToBackend(this.finalTranscript.trim());
          console.log("Final transcript:", this.finalTranscript);
          this.finalTranscript = ''; // Clear final transcript for next recording
        } else {
          interimTranscript += transcript;
        }
      }
      console.log("Interim transcript:", interimTranscript);
    }
  
    handleError(event) {
      console.error("Speech recognition error", event.error);
    }
  
    handleEnd() {
      this.isListening = false;
      console.log("Speech recognition ended");
      // Restart recognition if it ends unexpectedly
      this.start();
    }
  
    async sendToBackend(text) {
      try {
        const response = await fetch('http://127.0.0.1:8000/ai/text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 'text':text }),
        });
        const result = await response.json();
        console.log("Backend response:", result);
        console.log(text);
      } catch (error) {
        console.error("Error sending text to backend:", error);
      }
    }
  }
  
  // Usage
  const speechToText = new SpeechToText();
  speechToText.start();
  
  // To stop listening (if needed)
  // speechToText.stop();