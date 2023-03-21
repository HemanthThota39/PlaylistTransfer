

function updateProgressBar() {
  progressBar = document.getElementById("progressBar");
  fetch('/progress')
    .then(response => response.json())
    .then(data => {
        progressBar.setAttribute('value', data.fetched);
        progressBar.setAttribute('max', data.total);

    })
    .catch(error => console.log(error));
}

setInterval(updateProgressBar, 1000);

