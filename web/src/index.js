"use strict";

const axios = require('axios');

const storyboard = {
  "title": "ExampleTitle",
  "author": "Bernhard Brückenpfeiler",
  "frames": [
    {
      "scene": "001",
      "setting": "001",
      "section": "001",
      "timecode": "00:00:00:01",
      "image": "./example_image.png",
      "image_description": "Beschreibung des Bildes",
      "audio_description": "Beschreibung des Tons",
      "setting_size": "Halb Nah",
      "perspective": "Perspektive",
      "focal_length": "85",
      "camera_movement": "Statisch",
      "camera_support": "Stativ",
      "fx": "-"
    },
    {
      "scene": "002",
      "setting": "001",
      "section": "001",
      "timecode": "00:00:00:01",
      "image": "./example_image.png",
      "image_description": "Beschreibung des Bildes",
      "audio_description": "Beschreibung des Tons",
      "setting_size": "Halb Nah",
      "perspective": "Perspektive",
      "focal_length": "85",
      "camera_movement": "Statisch",
      "camera_support": "Stativ",
      "fx": "-"
    }
  ] 
}

const processStoryboard = (value) => {
  updateChuck();
  axios.get('http://127.0.0.1:8000/storyboard/', {
    params: {
      payload: JSON.parse(value)
    }
  })
  .then(function (response) {
    document.querySelector('#pdf-viewer').src = `http://127.0.0.1:8000/${response.data.path}`
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
    // always executed
  });
};


let ace = require("brace");
let timer = null;
require('brace/mode/javascript');
require('brace/theme/monokai');
ace.prototype = ace.edit("editor");
ace.prototype.getSession().setMode("ace/mode/javascript");
ace.prototype.setTheme("ace/theme/monokai");
let startContent = localStorage.lastStoryboard ? localStorage.lastStoryboard : JSON.stringify({
  storyboard
}, null, "\t");
ace.prototype.getSession().setValue(startContent);

ace.prototype.getSession().on("change", () => {
  if (timer) {
    clearTimeout(timer);
  }

  let value = ace.prototype.getSession().getValue();
  localStorage.lastStoryboard = value
  //timer = setTimeout(processStoryboard, 300);
});

document.querySelector('#process-button').addEventListener("click", () => {
  processStoryboard(ace.prototype.getSession().getValue()
)});


const updateChuck = () => {
  const url = "https://api.chucknorris.io/jokes/random";
  axios.get(url)
  .then(function (response) {
    document.querySelector('#chuck-norris').innerText = response.data.value
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
    // always executed
  });
}


updateChuck();
