let audio1 = new Audio(
    "https://s3-us-west-2.amazonaws.com/s.cdpn.io/242518/clickUp.mp3"
  );
  function chatOpen() {
    document.getElementById("chat-open").style.display = "none";
    document.getElementById("chat-close").style.display = "block";
    document.getElementById("chat-window1").style.display = "block";
  
    audio1.load();
    audio1.play();
  }
  function chatClose() {
    document.getElementById("chat-open").style.display = "block";
    document.getElementById("chat-close").style.display = "none";
    document.getElementById("chat-window1").style.display = "none";
    document.getElementById("chat-window2").style.display = "none";
  
    audio1.load();
    audio1.play();
  }
  function openConversation() {
    document.getElementById("chat-window2").style.display = "block";
    document.getElementById("chat-window1").style.display = "none";
  
    audio1.load();
    audio1.play();
  }
  
  //Gets the text from the input box(user)
  function userResponse() {
    let userText = document.getElementById("textInput").value;

  
    if (userText == "") {
      alert("Please type something!");
    } else {
      document.getElementById("messageBox").innerHTML += `<div class="first-chat">
        <p>${userText}</p>
        <div class="arrow"></div>
      </div>`;
      let audio3 = new Audio(
        "https://prodigits.co.uk/content/ringtones/tone/2020/alert/preview/4331e9c25345461.mp3"
      );
      audio3.load();
      audio3.play();
  
      var objDiv = document.getElementById("messageBox");
      objDiv.scrollTop = objDiv.scrollHeight;
  
      setTimeout(() => {
        adminResponse();
      }, 50);
    }
  }

  function adminResponse() {
    let message = document.getElementById("textInput").value;
    let button = document.getElementById("send");
    let url = button.getAttribute("data-url"); // Retrieve the URL from data-url
    const settings = {
      async: true,
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `message=${encodeURIComponent(message)}`, // Send the user's message as a POST parameter
    };
  
    fetch(url, settings)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the response as JSON
      })
      .then((data) => {
        const formattedResponse = data.response.replace(/\n/g, '<br>'); // Replace newline characters with HTML line breaks
        // Process the response data here
        $("#messageBox").append(`
          <div class="second-chat">
            <div class="circle" id="circle-mar"></div>
            <p>${formattedResponse}</p> <!-- Use data.response to access the assistant's message -->
            <div class="arrow"></div>
          </div>
        `);
  
        let audio3 = new Audio(
          "https://downloadwap.com/content2/mp3-ringtones/tone/2020/alert/preview/56de9c2d5169679.mp3"
        );
        audio3.load();
        audio3.play();
  
        var objDiv = document.getElementById("messageBox");
        objDiv.scrollTop = objDiv.scrollHeight;
      })
      .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
      });
  
    document.getElementById("textInput").value = "";
  }
  
  


// Event listener for sending user message on Enter key press

// Handle user input, send message to AI, and handle AI response
addEventListener("keypress", (e) => {
  if (e.keyCode === 13) {
      const inputElement = document.getElementById("textInput");
      if (inputElement === document.activeElement) {
          userResponse();
      }
  }
});
