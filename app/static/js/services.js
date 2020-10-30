export var SERVICES_CONTAINER = 'installed_services'

export class Service {

  constructor(api) {
    this.api = api;
    this.services = this.api.getServices();
    this.container = document.getElementsByClassName(SERVICES_CONTAINER)[0];
    this.generate();
  }

  generate() {
    this.container.innerHTML = "Installed Services";
    for (var i = 0; i < this.services.length; i++) {
      var serviceList = '\
      <div class="app_back">\
        <div class="services-info">\
        <img src="' + this.services[i].icon + '" class="services-icons-left">\
        <span id="' + i + '">' + this.services[i].name + '</span>\
        <img src="/system/static/img/trash-icon.png" id="' + i + '" class="services-icons-right trash">\
        <img src="/system/static/img/info-icon.png" id="' + i + '" class="services-icons-right">\
      </div>\
      '
      this.container.innerHTML += serviceList;
    }
    var elements = document.getElementsByClassName("trash");
    console.log(elements);
    for (var i = 0; i < elements.length; i++) {
      elements[i].onclick = function(serviceObject, id) {
        return function() {
          serviceObject.deleteService(id);
        };
      }(this, i);
    }
  }

  deleteService(id) {
    var dockerId = this.services[id].dockerId;
    var is_Deleted = this.api.deleteService(dockerId);
    if(is_Deleted){
      console.log("deleted");
    } else {
      console.log("error");
    }
    this.services = this.api.getServices();
    this.generate();
  }

}
