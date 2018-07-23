// Runs the given query and fetches the first result.
// Args:
// - query: the string to use for the query.
// - resultCallback: a function to call when the results are available.
//                   Should take a single argument: the JSON returned from
//                   giphy's API
function queryGiphy(query, resultCallback) {
  // The giphyAPiKey is now stored on the server
  jQuery.get("/get_image?query="+query, resultCallback)
}

// Makes the element with ID 'resultPane' visible, and sets the element with ID
// 'result' to contain the resultUrl returned from our application
function displayResult(resultUrl) {
  var resultPaneDiv = document.querySelector('#resultPane')
  var resultDiv = document.querySelector('#result')
  var imgString = "<img src='" + resultUrl + "'/>"
  resultDiv.innerHTML = imgString

  // This line makes the container for the result div and the "add to favorites"
  // button visible.
  resultPaneDiv.style.display = "block"
}

// contacts our server, and asks it to add gifUrl to the list of favorite GIFs.
// doneCallback should be a function, which addGifToFavorites will invoke when
// the gifUrl is saved successfully.
function addGifToFavorites(gifUrl, doneCallback) {
  jQuery.post("/add_favorite", {url: gifUrl}, doneCallback);
}

// TODO: Create an event handler for when the button is clicked
// that calls queryGiphy using the displayResult function as the callback

function submitClick() {
  var inputBox = document.querySelector('#queryBox')
  var userInput = inputBox.value
  queryGiphy(userInput, displayResult)
}

function addFavoriteClick() {
  addGifToFavorites(currentGifUrl, () => {
    alert("saved!")
  })
}

window.addEventListener('load', () => {
  document.querySelector('#submit').addEventListener("click", submitClick)
  document.querySelector('#addFavorite').addEventListener('click', addFavoriteClick)
});
