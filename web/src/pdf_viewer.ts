import { EditorEventListener } from "./event/EventListener";
import { EditorEventHub } from "./event/EventHub";
import { EditorEvent, EventType } from "./event/Event";

export class PdfViwer implements EditorEventListener{
  static instance: PdfViwer;
  root: HTMLIFrameElement;

  constructor(root: HTMLIFrameElement) {
    this.root = root;
    EditorEventHub.subscribe(this);
  }

  static getInstance() {
    if (!PdfViwer.instance) {
      PdfViwer.instance = new PdfViwer(document.querySelector("#pdf-viewer"));
    }
    return PdfViwer.instance;
  }

  setPdf(path: string) {
    this.root.src = path;
  }

  comsumeEvent(event: EditorEvent) {
    if (event.type == EventType.RENDER_FINISH_EVENT) {
      this.setPdf(event.data["pdf_path"]);
    }
  }
}