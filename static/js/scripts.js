window.onload = function () {
  const replInput = document.getElementById('repl-input');
  const replOutput = document.getElementById('repl-output');
  const markdownEditor = document.getElementById('markdown-editor');
  replInput.addEventListener('keydown', function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      const code = replInput.value;
      replInput.value = '';
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
          } else {
            replOutput.value += '\nError: ' + data.message;
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }
  });
  markdownEditor.addEventListener('keydown', function (event) {
    if (event.key === "Tab") {
      event.preventDefault();
      const start = this.selectionStart;
      const end = this.selectionEnd;
      this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
      this.selectionStart = this.selectionEnd = start + 1;
    }
  });
}