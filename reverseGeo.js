// Initial setup variables
const csvToJson = require('convert-csv-to-json'); 
const axios = require('axios').default;
let API_KEY = "AIzaSyD-Fwlf4-W04pkqjQly5kcP3VNfRSGWn2w";

// Variables for when valid addresses are found
let foundAddresses = {
  "addresses" : []
};
var numAddresses = 0;
var max = 10;

// Convert csv to json
let json = csvToJson.fieldDelimiter(',').getJsonFromCsv("./csv/housing copy.csv");

function main () {
  // Loop to find the addresses
  for(let i = 0; i < Object.keys(json).length && numAddresses < max; ++i) {
    let coordinates = `${json[i].latitude},${json[i].longitude}`;

    getAddress(coordinates, i)
    .then(({result, row}) => {
      if (result != null && isValidAddress(result) && numAddresses < max) {
        ++numAddresses;
        row = row.toString();
        foundAddresses['addresses'].push({row : result});
        console.log("GOT A HIT: " + numAddresses + " for " + result);
        console.log(foundAddresses.addresses);
      }  
    })
    .catch((error) => {});
  }
}

async function getAddress(coordinates, index) {
  try {
    const response = await axios.get(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${coordinates}&key=${API_KEY}`);
    let address = response.data.results[0].formatted_address;
    return {result: address, row: index};
  } 
  catch (error) {
    return;
  }
}

// Checks if an address is valid
function isValidAddress(address) {
  let splitAddress = address.split(" ");
  
  // If the first index contains only digits, return true
  if (splitAddress[0].match(/[^0-9]/) == null) {
    return true;
  }
  
  return false;
}

main()