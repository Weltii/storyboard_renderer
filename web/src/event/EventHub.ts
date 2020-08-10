import { EditorEventListener } from "./EventListener";
import { EditorEvent } from "./Event";

export class EditorEventHub {
  static listeners = [];

  static subscribe(listener: EditorEventListener) {
    if (EditorEventHub.listeners.indexOf(listener) < 0) {
      EditorEventHub.listeners.push(listener);
    }
  }

  static unsubscribe(listener: EditorEventListener) {
    const index = EditorEventHub.listeners.indexOf(listener);
    if (index < 0) {
      EditorEventHub.listeners.splice(index, 1);
    }
  }

  static sendEvent(editorEvent: EditorEvent) {
    EditorEventHub.listeners.forEach((listener: EditorEventListener) => {
      if (editorEvent.sender != listener) {
        listener.comsumeEvent(editorEvent);
      }
    });
  }
}
