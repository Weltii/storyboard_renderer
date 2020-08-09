export class ProjectManager {
  root: HTMLElement;
  projectTitle: HTMLElement;
  pathChooser: HTMLInputElement;
  loadButton: HTMLButtonElement;
  createButton: HTMLButtonElement;
  closeButton: HTMLButtonElement;
  currentPath: string = "";

  constructor(root: HTMLElement) {
    this.root = root;
    this.projectTitle = root.querySelector('#project-title')
    this.pathChooser = root.querySelector('#project-path')
    this.loadButton = root.querySelector('#project-load-button')
    this.createButton = root.querySelector('#project-create-button')
    this.closeButton = root.querySelector('#project-close-button')

    this.pathChooser.addEventListener("change", this.onPathChooserChange)
    this.loadButton.addEventListener("click", this.onLoadButtonClick);
    this.createButton.addEventListener("click", this.onCreateButtonClick);
    this.closeButton.addEventListener("click", this.onCloseButtonClick);
  }

  onPathChooserChange(event: Event) {
    //@ts-ignore
    console.log(event.target.value);
  }
  
  onLoadButtonClick() {
    // TODO handle project loading!
    console.warn(`project loading is not implemented!`);
  }

  onCreateButtonClick() {
    // TODO handle project loading!
    console.warn(`project creation is not implemented!`);
  }

  onCloseButtonClick() {
    // TODO handle project loading!
    console.warn(`closing projects is not implemented!`);
  }
}