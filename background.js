// background.js

chrome.runtime.onInstalled.addListener(() => {
  console.log("Your guide Kanha is now ready to help you out!!!");
});

chrome.runtime.onSuspend.addListener(() => {
  console.log("Popup is closing, clearing ChromaDB...");

  fetch('http://127.0.0.1:5000/clear_chromadb', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          console.log(data.message);
      } else {
          console.error("Error clearing ChromaDB");
      }
  })
  .catch(error => {
      console.error("Error:", error);
  });
});
