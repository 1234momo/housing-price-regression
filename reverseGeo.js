// Initial setup variables
const csvToJson = require('convert-csv-to-json'); 
const axios = require('axios').default;
let API_KEY = "AIzaSyD-Fwlf4-W04pkqjQly5kcP3VNfRSGWn2w";
var stringify = require('csv-stringify');
var fs = require('fs');


// Variables for when valid addresses are found
let foundAddresses = {
  "addresses" : []
};
foundAddresses['addresses'].push(["row", "address"]);
var numAddresses = 0;
var max = Number.MAX_VALUE;

// Convert csv to json
let json = csvToJson.fieldDelimiter(',').getJsonFromCsv("./csv/housing.csv");

function main () {
  // Loop to find the addresses
  for(let i = 0; i < Object.keys(json).length; ++i) {
    let coordinates = `${json[i].latitude},${json[i].longitude}`;

    getAddress(coordinates, i)
    .then(({result, row}) => {

      // If result is a string, valid address, and the max hasn't been reached, add the address into foundAddresses
      if (result !== null && isValidAddress(result)) {
        ++numAddresses;
        let observation = [];
        observation.push(row); 
        observation.push(result);
        foundAddresses['addresses'].push(observation);

        console.log("GOT A HIT: " + numAddresses + " for " + result);
        console.log(foundAddresses.addresses);
      }  

      // Save JSON into CSV
        stringify(foundAddresses.addresses, function(err, output) {
          fs.writeFile('name2.csv', output, 'utf8', function(err) {
            if (err) {
              console.log('Some error occured - file either not saved or corrupted file saved.');
            } else {
              console.log('It\'s saved!');
            }
          });
        });
    })
    .catch((error) => {});
  }
}

// Get address associated with coordinates object, where coordinates={latitude,longitude}
async function getAddress(coordinates, index) {
  try {
    const response = await axios.get(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${coordinates}&key=${API_KEY}`);
    let address = response.data.results[0].formatted_address;
    return {result: address, row: index.toString()};
  } 
  catch (error) {
    return;
  }
}

// Checks if an address is valid
function isValidAddress(address) {
  let splitAddress = address.split(" ");
  
  // If the first index contains only digits, return true
  if (splitAddress[0].match(/[^0-9]/) === null) {
    return true;
  }
  
  return false;
}

// Start of program
main();
