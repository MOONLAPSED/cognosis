window.onload = function () {
  const markdownEditor = document.getElementById('markdown-editor');
  const markdownPreview = document.getElementById('markdown-preview');
  const replInputButton = document.getElementById('repl-input');
  const replOutput = document.getElementById('repl-output');

  // Markdown-it instance for rendering markdown text 
  const md = window.markdownit();

  // Event listener for updating the Markdown preview on input
  markdownEditor.addEventListener('input', function () {
    const markdownText = markdownEditor.value;
    const htmlText = md.render(markdownText);
    markdownPreview.innerHTML = htmlText; // Update the preview pane with the HTML output
  });

  // REPL button to send markdown content to server and receive processed output
  replInputButton.addEventListener('click', function () {
    const code = markdownEditor.value; // get markdown content

    fetch('/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ instruct: code }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          replOutput.value += '\n' + data.message;
          markdownPreview.innerHTML = ''; // Optionally also clear markdown preview
        } else {
          replOutput.value += '\nError: ' + data.message;
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        replOutput.value += '\nError: ' + error;
      });
  });

  // Enable tab usage in markdown editor
  markdownEditor.addEventListener('keydown', function (event) {
    if (event.key === "Tab") {
      event.preventDefault();
      const start = this.selectionStart;
      const end = this.selectionEnd;
      this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
      this.selectionStart = this.selectionEnd = start + 1;
    }
  });
};