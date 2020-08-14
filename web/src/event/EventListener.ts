import { EditorEvent } from "./Event";

export interface EditorEventListener {
  consumeEvents(event: EditorEvent): void;
}
