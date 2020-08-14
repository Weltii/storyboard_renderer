import { BackendService } from "./backend_service";
import { EditorEventListener } from "./event/EventListener";
import { EditorEvent, EventType } from "./event/Event";
import { EditorEventHub } from "./event/EventHub";

export class OverlayMenu implements EditorEventListener {
  root: HTMLElement;
  saveButton: HTMLButtonElement;
  renderButton: HTMLButtonElement;
  layoutSelection: HTMLSelectElement;
  currentLayout: string;

  constructor(root: HTMLElement) {
    this.root = root;
    this.saveButton = root.querySelector("#save-button");
    this.saveButton.addEventListener(
      "click",
      this.onSaveButtonClick.bind(this)
    );

    this.renderButton = root.querySelector("#render-button");
    this.renderButton.addEventListener(
      "click",
      this.onRenderButtonClick.bind(this)
    );

    this.layoutSelection = root.querySelector("#layout-selection");
    this.layoutSelection.addEventListener(
      "change",
      this.onLayoutSelectionChange.bind(this)
    );

    this.fillLayoutSelection();
    EditorEventHub.subscribe(this);
  }

  onSaveButtonClick() {
    EditorEventHub.sendEvent(new EditorEvent(EventType.SAVE_EVENT, {}, this));
  }

  onRenderButtonClick() {
    EditorEventHub.sendEvent(new EditorEvent(EventType.RENDER_EVENT, {}, this));
    this.renderButton.disabled = true;
  }

  onLayoutSelectionChange(event: Event) {
    //@ts-ignore
    const value = event.target.value;
    this.setLayout(value);
  }

  private async fillLayoutSelection() {
    const response = await BackendService.getAllLayouts();
    if (response.status == 200) {
      const layouts = response.data;
      layouts.forEach((layout: string) => {
        let option: HTMLOptionElement = document.createElement("option");
        option.value = layout;
        option.innerText = layout.replace("_", " ");
        this.layoutSelection.appendChild(option);

        if (!this.currentLayout) {
          this.setLayout(layout);
        }
      });
    } else {
      console.error("Something went wrong by getting all layouts!");
    }
  }

  private setLayout(layout: string) {
    this.currentLayout = layout;
  }

  consumeEvents(event: EditorEvent) {
    switch(event.type) {
      case EventType.RENDER_FINISH_EVENT:
        this.renderButton.disabled = false;
        break;
    }
  }
}
