const csvToJson = require('convert-csv-to-json'); 
const axios = require('axios').default;
let API_KEY = "AIzaSyD-Fwlf4-W04pkqjQly5kcP3VNfRSGWn2w";

// Convert csv to json
let json = csvToJson.fieldDelimiter(',').getJsonFromCsv("./csv/housing.csv");

// Test 1 coordinate
let coordinates = `${json[1].latitude},${json[1].longitude}`;

console.log("\'" + coordinates + "\'");
getAddress(coordinates);

async function getAddress(coordinates) {
    try {
      const response = await axios.get(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${coordinates}&key=${API_KEY}`);
      console.log(response.data.results);
    } catch (error) {
      console.error(error);
    }
  }