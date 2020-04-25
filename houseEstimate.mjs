const Zillow = require("node-zillow");
const fetch = require("node-fetch");
const zillow = new Zillow('X1-ZWz179fm6hk64r_5taq0');
const axios = require('axios').default;
import foundAddresses from './reverseGeo.js';

function main() {
    // let json;

    // fetch("name.csv")
    // .then(res => res.json())
    // .then(data => json = data)
    // .catch(err => console.error(err));
    
    console.log(foundAddresses);

    // for (let i = 0; i < Object.keys(json).length; ++i) {
    //     let splitData = json[i].split(",", 1);
    //     fetchZestimate()
    // }
}

//var csv is the CSV file with headers
function csvJSON(csv){

    var lines=csv.split("\n");
  
    var result = [];
  
    // NOTE: If your columns contain commas in their values, you'll need
    // to deal with those before doing the next step 
    // (you might convert them to &&& or something, then covert them back later)
    // jsfiddle showing the issue https://jsfiddle.net/
    var headers=lines[0].split(",", 1);
  
    for(var i = 1; i < lines.length; i++){
  
        let obj = {};
        let currentline = lines[i].split(",", 1);
  
        for(let j = 0; j < headers.length; j++){
            obj[headers[j]] = currentline[j];
        }
  
        result.push(obj);
    }
  
    //return result; //JavaScript object
    return JSON.stringify(result); //JSON
}

async function fetchZestimate(searchAddress, searchCityStateZip) {
    const parameters = {
        address: searchAddress,
        citystatezip: searchCityStateZip,
        rentzestimate: false
    }
    
    zillow.get('GetSearchResults', parameters)
        .then(results => {
            console.log(results)
            return results
        })
}

main();