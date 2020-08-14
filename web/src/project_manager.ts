import { BackendService } from "./backend_service";
import { NotificationHandler, LogLevel } from "./notification_handler";
import { AceBrdige } from "./ace_bridge";
import { OverlayMenu } from "./overlay_menu";
import { Project } from "./classes/project";
import { EditorEventListener } from "./event/EventListener";
import { EditorEvent, EventType } from "./event/Event";
import { EditorEventHub } from "./event/EventHub";

export class ProjectManager implements EditorEventListener {
  root: HTMLElement;
  projectTitle: HTMLInputElement;
  pathChooser: HTMLInputElement;
  loadButton: HTMLButtonElement;
  createButton: HTMLButtonElement;
  closeButton: HTMLButtonElement;
  currentPath: string = "";
  notificationHandler: NotificationHandler;
  aceBridge: AceBrdige;
  overlayMenu: OverlayMenu;
  currentProject: Project;
  currentLayout: string;
  isRendering: boolean;

  constructor(
    root: HTMLElement,
    aceBridge: AceBrdige,
    overlayMenu: OverlayMenu
  ) {
    this.root = root;
    this.projectTitle = root.querySelector("#project-title");
    this.pathChooser = root.querySelector("#project-path");
    this.loadButton = root.querySelector("#project-load-button");
    this.createButton = root.querySelector("#project-create-button");
    this.closeButton = root.querySelector("#project-close-button");

    this.pathChooser.addEventListener(
      "change",
      this.onPathChooserChange.bind(this)
    );
    this.loadButton.addEventListener(
      "click",
      this.onLoadButtonClick.bind(this)
    );
    this.createButton.addEventListener(
      "click",
      this.onCreateButtonClick.bind(this)
    );
    this.closeButton.addEventListener(
      "click",
      this.onCloseButtonClick.bind(this)
    );

    this.notificationHandler = NotificationHandler.getInstance();
    this.currentPath = this.pathChooser.value;

    this.aceBridge = aceBridge;
    this.overlayMenu = overlayMenu;
    this.overlayMenu.onSaveButtonClick = this.saveProject.bind(this);

    EditorEventHub.subscribe(this);

    this.getDefaultLayout();
  }

  onPathChooserChange(event: Event) {
    //@ts-ignore
    this.currentPath = event.target.value;
  }

  async onLoadButtonClick() {
    let response: any = await BackendService.getProject(this.currentPath);
    if (response.status == 200) {
      this.notificationHandler.addNotification(
        "Load project",
        "Project successfuly loaded",
        LogLevel.LOG
      );
      this.projectTitle.value = response.data.storyboard.title;
      this.pathChooser.value = response.data.path;
      this.aceBridge.setText(
        JSON.stringify(response.data.storyboard, null, "\t")
      );
    } else {
      this.notificationHandler.addNotification(
        "Load project failed",
        response.data.detail,
        LogLevel.ERROR
      );
    }
  }

  async onCreateButtonClick() {
    let response: any = await BackendService.createProject(this.currentPath);
    if (response.status == 200) {
      this.notificationHandler.addNotification(
        "Create project",
        "Project successfuly created",
        LogLevel.LOG
      );
      this.projectTitle.value = response.data.storyboard.title;
      this.pathChooser.value = response.data.path;
      this.aceBridge.setText(
        JSON.stringify(response.data.storyboard, null, "\t")
      );
    } else {
      this.notificationHandler.addNotification(
        "Create project failed",
        response.data.detail,
        LogLevel.ERROR
      );
    }
  }

  async onCloseButtonClick() {
    let response: any = await BackendService.closeProject();
    if (response.status == 200) {
      this.notificationHandler.addNotification(
        "Close project",
        "Project successfuly closed",
        LogLevel.LOG
      );
      this.projectTitle.value = "";
      this.aceBridge.setText();
    } else {
      this.notificationHandler.addNotification(
        "Close project failed",
        response.data.detail,
        LogLevel.ERROR
      );
    }
  }

  async saveProject() {
    let response: any = await BackendService.saveStoryboard(
      JSON.parse(this.aceBridge.getText())
    );
    if (response.status == 200) {
      let job = response.data;
      this.checkErrorsInJob(job);
    } else {
      this.notificationHandler.addNotification(
        "Save project failed",
        response.data.detail,
        LogLevel.ERROR
      );
    }
  }

  async renderProject() {
    if (this.isRendering) {
      return;
    }
    this.isRendering = true;
    let response: any = await BackendService.renderProject();
    if (response.status == 200) {
      this.getBase64Pdf(response.data.pdf_file_path)
    } else {
      this.notificationHandler.addNotification(
        "Render storyboard failed",
        `We work on a more detailed solution.\n${response.data.detail}`,
        LogLevel.ERROR
      );
    }
    this.isRendering = false;
  }

  async getBase64Pdf(path: string) {
    let response = await BackendService.getBase64Pdf(path);
    if (response.status == 200) {
      EditorEventHub.sendEvent(new EditorEvent(EventType.RENDER_FINISH_EVENT, {
        pdf_path: response.data.pdf
      }, this));
    } else {
      this.notificationHandler.addNotification(
        "PDF not found",
        `No .pdf found, please render again.`,
        LogLevel.ERROR
      );
    }
  }

  comsumeEvent(event: EditorEvent) {
    switch (event.type) {
      case EventType.SAVE_EVENT:
        this.saveProject();
        break;
      case EventType.RENDER_EVENT:
        this.renderProject();
        break;
    }
  }

  private async getDefaultLayout() {
    const response = await BackendService.getAllLayouts();
    if (response.status == 200) {
      const layouts = response.data;
      this.currentLayout = layouts[0];
    } else {
      console.error("Something went wrong by getting all layouts!");
    }
    this.currentLayout = "InvalidLayout"
  }

  private checkErrorsInJob(job: any) {
      switch (job.status) {
        case "valid":
          this.notificationHandler.addNotification(
            "Save project",
            "Project successfuly saved",
            LogLevel.LOG
          );
          break;
        case "invalid_data": 
          const wrongData = job.status_data.wrong_data_type || null;
          const missingData = job.status_data.missing_data || null;
          let message = "Your data are invalid:\n"
          if (wrongData) {
            message += "Wrong data:\n"
            wrongData.forEach(element => {
              message += `Frame ${element.frame}: ${element.message}\n`;
            });
          }
          if (missingData) {
            message += "Missing data:\n"
            missingData.forEach(element => {
              message += `Frame ${element.frame}: ${element.message}\n`;
            });
          }
          this.notificationHandler.addNotification(
            "Save Project",
            message,
            LogLevel.ERROR
          )
          break;
        case "generate_tex_error":
          this.notificationHandler.addNotification(
            "Save Project",
            "Something goes wrong at the .tex file generation.",
            LogLevel.ERROR
          )
          break;
        case "compile_pdf_error":
          this.notificationHandler.addNotification(
            "Save Project",
            "The .tex file cannot compile.",
            LogLevel.ERROR
          )
          break;
        case "unknown_error":
          this.notificationHandler.addNotification(
            "Save Project",
            "Unknown error",
            LogLevel.ERROR
          )
          break;
      }
  }
}
