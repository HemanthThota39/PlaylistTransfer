const progressbar = document.querySelector('#progressBar');
const transferBtn = document.querySelector('#transfer-btn');

function updateProgressBar() {
  fetch('/progress')
    .then(response => response.json())
    .then(data => {
      const progress = (data.fetched / data.total) * 100;
      progressBar.setAttribute('value', progress);
    })
    .catch(error => console.log(error));
}

// hide the progress bar initially
progressbar.style.display = 'none';

// add event listener to transfer button
transferBtn.addEventListener('click', () => {
  // show the progress bar
  progressbar.style.display = 'block';
  // call updateProgressBar() every 5 seconds
  setInterval(updateProgressBar, 5000);
});
