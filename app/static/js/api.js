import  {Tuser} from "./Tuser.js"
import  {Tservice} from "./Tservice.js"

export var API_PATH = '/system/api/';

export class Request{

  constructor(token) {
    this.token = token;
    this.api_path = API_PATH;
  }

  getServices() {
    var servicesList = [];
    var request = this.getJson(this.api_path + "list");
    for (var i = 0; i < request.service.length; i++) {
      var serviceObject = new Tservice(
        request.service[i].name,
        request.service[i].docker_id,
        request.service[i].is_visible,
        request.service[i].super,
        request.service[i].is_required,
        request.service[i].path,
        request.service[i].icon);
      servicesList.push(serviceObject);
    }
    return servicesList;
  }

  deleteService(dockerId){
    var success = false;
    var json;
    var request = new XMLHttpRequest();
    request.open("POST", this.api_path + "remove/?service_id=" + dockerId, false);
    request.send(null);
    json = JSON.parse(request.responseText);
    if(json.status == "success"){
      success = true;
    }
    return success;
  }

  getJson(url) {
    var json;
    var request = new XMLHttpRequest();
    request.open("GET", url, false);
    request.send(null);
    json = JSON.parse(request.responseText);
    return json;
  }
}
