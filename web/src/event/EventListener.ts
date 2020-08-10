import { EditorEvent } from "./Event";

export interface EditorEventListener {
  comsumeEvent(event: EditorEvent): void;
}
