export class Tservice {

  constructor(name,dockerId, isVisible, isAdmin, isRequired, path, icon) {
    this.name = name;
    this.dockerId = dockerId;
    this.isVisible = isVisible;
    this.isAdmin = isAdmin;
    this.isRequired = isRequired;
    this.path = path;
    this.icon = icon;
  }

  
}
