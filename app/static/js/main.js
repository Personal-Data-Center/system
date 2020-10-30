import * as api from './api.js'
import * as service from './services.js'

var TOKEN = "testtest";
var apiObject;
var serviceObject;
function test(id){
  console.log(id);
}
document.addEventListener('DOMContentLoaded', function() {
  apiObject = new api.Request(TOKEN);
  serviceObject = new service.Service(apiObject);
}, false);
