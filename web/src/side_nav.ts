import { EditorEventListener } from "./event/EventListener";
import { EditorEvent, EventType } from "./event/Event";
import { EditorEventHub } from "./event/EventHub";

export class SideNav implements EditorEventListener{
  private root: HTMLElement;
  private openButton: HTMLElement;
  private closeButton: HTMLElement;

  constructor(navRoot: HTMLElement, openButton: HTMLElement) {
    this.root = navRoot;
    this.openButton = openButton;
    this.openButton.addEventListener("click", this.open.bind(this));
    this.closeButton = navRoot.querySelector(".close-button");
    this.closeButton.addEventListener("click", this.close.bind(this));

    EditorEventHub.subscribe(this);
  }

  open() {
    this.root.classList.add("open");
  }

  close() {
    this.root.classList.remove("open");
  }

  consumeEvents(event: EditorEvent) {
    if (event.type == EventType.NEW_NOTIFICATION) {
      const name = `highlight-${event.data["logLevel"]}`
      this.openButton.classList.add(name);

      setTimeout(() => {
        this.openButton.classList.remove(name);
      }, 1000)
    }
  }
}
