import { BackendService } from "./backend_service";
import { NotificationHandler, LogLevel } from "./notification_handler";
import { AceBrdige } from "./ace_bridge";

export class ProjectManager {
  root: HTMLElement;
  projectTitle: HTMLInputElement;
  pathChooser: HTMLInputElement;
  loadButton: HTMLButtonElement;
  createButton: HTMLButtonElement;
  closeButton: HTMLButtonElement;
  currentPath: string = "";
  notificationHandler: NotificationHandler;

  constructor(root: HTMLElement, aceBridge: AceBrdige) {
    this.root = root;
    this.projectTitle = root.querySelector('#project-title')
    this.pathChooser = root.querySelector('#project-path')
    this.loadButton = root.querySelector('#project-load-button')
    this.createButton = root.querySelector('#project-create-button')
    this.closeButton = root.querySelector('#project-close-button')

    this.pathChooser.addEventListener("change", this.onPathChooserChange.bind(this))
    this.loadButton.addEventListener("click", this.onLoadButtonClick.bind(this));
    this.createButton.addEventListener("click", this.onCreateButtonClick.bind(this));
    this.closeButton.addEventListener("click", this.onCloseButtonClick.bind(this));

    this.notificationHandler = NotificationHandler.getInstance();
    this.currentPath = this.pathChooser.value;
  }

  onPathChooserChange(event: Event) {
    //@ts-ignore
    this.currentPath = event.target.value;
  }
  
  async onLoadButtonClick() {
    let response: any = await BackendService.getProject(this.currentPath);
    console.log(response);
    if (response.status == 200) {
      this.notificationHandler.addNotification("Load project", "Project successfuly loaded", LogLevel.LOG)
      this.projectTitle.value = response.data.storyboard.title;
      this.pathChooser.value = response.data.path;
    }
    else {
      this.notificationHandler.addNotification("Load project failed", response.data.detail, LogLevel.ERROR);
    }
  }

  async onCreateButtonClick() {
    let response: any = await BackendService.createProject(this.currentPath);
    if (response.status == 200) {
      this.notificationHandler.addNotification("Create project", "Project successfuly created", LogLevel.LOG)
      this.projectTitle.value = response.data.storyboard.title;
      this.pathChooser.value = response.data.path;
    }
    else {
      this.notificationHandler.addNotification("Create project failed", response.data.detail, LogLevel.ERROR);
    }
  }

  async onCloseButtonClick() {
    let response: any = await BackendService.closeProject();
    console.log(response);
    if (response.status == 200) {
      this.notificationHandler.addNotification("Close project", "Project successfuly closed", LogLevel.LOG)
      this.projectTitle.value = "";
    }
    else {
      this.notificationHandler.addNotification("Close project failed", response.data.detail, LogLevel.ERROR);
    }
  }
}