import { EditorEventListener } from "./EventListener";

export enum EventType {
  SAVE_EVENT = "save_event",
  RENDER_EVENT = "render_event",
  RENDER_FINISH_EVENT = "render_finish_event",
  NEW_NOTIFICATION = "new_notivication"
}

export class EditorEvent {
  type: EventType;
  data: { key: { key: any } };
  sender: EditorEventListener;

  constructor(type: EventType, data: any, sender: EditorEventListener = null) {
    this.type = type;
    this.data = data;
    this.sender = sender;
  }
}
