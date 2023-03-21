// get reference to the progress bar
function update()
{const progressBar = document.getElementById("progressBar");

// make a GET request to retrieve the progress data
fetch("/progress")
  .then(response => response.json())
  .then(data => {
    // update the progress bar's value and max attributes
    progressBar.value = data.fetched;
    progressBar.max = data.total;

    // update the progress text (assuming you have an element with an id of "progressText")
    document.getElementById("progressText").textContent = data.progress;

    // log the progress to the console (optional)
    console.log(`Progress: ${data.progress}/${data.total}`);
  })
  .catch(error => {
    console.error(`Error retrieving progress: ${error}`);
  });
}
setInterval(update, 1000)
