const csvToJson = require('convert-csv-to-json'); 
const axios = require('axios').default;
let API_KEY = "AIzaSyD-Fwlf4-W04pkqjQly5kcP3VNfRSGWn2w";

// Convert csv to json
let json = csvToJson.fieldDelimiter(',').getJsonFromCsv("./csv/housing.csv");

for (let i = 0; i < Object.keys(json).length; ++i) {
  let coordinates = `${json[i].latitude},${json[i].longitude}`;
  getAddress(coordinates, i+1);
}

async function getAddress(coordinates, index) {
  try {
    const response = await axios.get(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${coordinates}&key=${API_KEY}`);
    console.log(index + ": " + response.data.results[0].formatted_address);
  } 
  catch (error) {
    console.error(index + ": Unable to locate");
    // console.error(error);
  }
}