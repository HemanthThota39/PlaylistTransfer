// select the progress bar element
const progressBar = document.querySelector('progress')
function updateProgressBar(){
    // make an AJAX request to fetch progress data from the server
    fetch('/progress')
    .then(response => response.json())
    .then(data => {
        const progress = (data.fetched / data.total) * 100;
        progressBar.setAttribute('value', progress);
    })
    .catch(error => console.log(error))
}
console.log("Working")
setInterval(updateProgressBar, 1000)