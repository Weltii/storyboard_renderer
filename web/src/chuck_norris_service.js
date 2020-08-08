const axios = require('axios');

export class ChuckNorrisWorker { 
  intervalTime = 10 // seconds
  url = "https://api.chucknorris.io/jokes/random";
  
  constructor() {
    this.progressForeground = document.querySelector(".progress-foreground")
    this.jokeElement = document.querySelector("#joke")
    this.getJoke()
    this.timer = setInterval(this.getJoke.bind(this), this.intervalTime * 1000)
  }

  distributeJoke(joke) {
    this.progressForeground.style.display = "none"
    this.jokeElement.innerHTML = joke;
    setTimeout(() => {
      this.progressForeground.style.display = "block"
    }, 16);
  }

  getJoke() { 
    axios.get(this.url)
    .then(function (response) {
      this.distributeJoke(response.data.value)
    }.bind(this));
  }
}