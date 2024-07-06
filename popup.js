document.addEventListener('DOMContentLoaded', async () => {
    const queryInput = document.getElementById('query');
    const getAnswerButton = document.getElementById('getAnswer');
    const answerTextarea = document.getElementById('answer');
  
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const currentTabUrl = tab.url;
  
    // Preload content when the popup is opened
    await preloadContent(currentTabUrl);
  
    getAnswerButton.addEventListener('click', async () => {
      const query = queryInput.value;
      if (query) {
        getAnswer(query);
      } else {
        alert("Please enter a question.");
      }
    });
  
    async function preloadContent(url) {
      const response = await fetch('http://127.0.0.1:5000/preload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
      });
      const result = await response.json();
      if (result.message) {
        console.log(result.message);
      } else {
        console.error("Error preloading content");
      }
    }
  
    async function getAnswer(query) {
      const response = await fetch('http://127.0.0.1:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query })
      });
      const result = await response.json();
      if (result.answer) {
        answerTextarea.value = result.answer;
      } else {
        answerTextarea.value = "Error fetching answer.";
      }
    }
  });
  