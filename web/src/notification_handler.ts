import { EditorEventHub } from "./event/EventHub";
import { EditorEvent, EventType } from "./event/Event";

export enum LogLevel {
  LOG = "log",
  ERROR = "error",
  WARN = "warn",
}

class Notification {
  root: HTMLElement;
  removeButton: HTMLButtonElement;
  title: HTMLElement;
  content: HTMLSpanElement;

  constructor(title: string, content: string, logLevel: LogLevel) {
    this.root = document.createElement("div");
    this.root.classList.add(logLevel);
    this.removeButton = document.createElement("button");
    this.removeButton.innerText = "X";
    this.removeButton.classList.add("close-button");
    this.removeButton.addEventListener("click", this.remove.bind(this));

    this.title = document.createElement("h3");
    this.title.innerText = title;

    this.content = document.createElement("span");
    this.content.innerText = content;

    this.root.appendChild(this.removeButton);
    this.root.appendChild(this.title);
    this.root.appendChild(this.content);
  }

  remove() {
    this.root.parentElement.removeChild(this.root);
  }
}

export class NotificationHandler {
  static instance: NotificationHandler;

  root: HTMLElement;
  removeAllButton: HTMLButtonElement;
  notificationArea: HTMLElement;

  static getInstance() {
    if (!NotificationHandler.instance) {
      NotificationHandler.instance = new NotificationHandler();
    }
    return NotificationHandler.instance;
  }

  constructor() {
    this.root = document.querySelector("#notification-area");
    this.notificationArea = this.root.querySelector("#notifications");
    this.removeAllButton = this.root.querySelector("#notifications-remove-all");
    this.removeAllButton.addEventListener("click", () => {
      this.removeChilds(this.notificationArea);
    });
  }

  private removeChilds(parent: HTMLElement) {
    while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
    }
  }

  addNotification(
    title: string,
    content: string,
    logLevel: LogLevel = LogLevel.LOG
  ) {
    let notification = new Notification(title, content, logLevel);
    this.notificationArea.appendChild(notification.root);
    EditorEventHub.sendEvent(new EditorEvent(EventType.NEW_NOTIFICATION, {}))
  }
}
