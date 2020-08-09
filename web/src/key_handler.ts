class Key {
  name: string;
  key: number | string;

  constructor(name: string, key: number | string) {
    this.name = name;
    this.key = key;
  }
}

export class KeyHandler {
  static CTRL_BUTTONS = [new Key("ctrl_save", 83)];
  static SHIFT_BUTTONS = [];
  static instance: KeyHandler;

  listeners: [] = [];

  static getInstance() {
    if (!KeyHandler.instance) {
      KeyHandler.instance = new KeyHandler();
    }
    return KeyHandler.instance;
  }

  private constructor() {
    document.onkeydown = this.listenOnKey.bind(this);
  }

  listenOnKey(event: KeyboardEvent) {
    KeyHandler.CTRL_BUTTONS.forEach((key: Key) => {
      if ((event.ctrlKey && event.key == key.key) || event.keyCode == key.key) {
        event.preventDefault();
        this.callEvent(key);
        return;
      }
    });
    KeyHandler.SHIFT_BUTTONS.forEach((key: Key) => {
      if (
        (event.shiftKey && event.key == key.key) ||
        event.keyCode == key.key
      ) {
        event.preventDefault();
        this.callEvent(key);
        return;
      }
    });
  }

  callEvent(key: Key) {
    if (this.listeners[key.name]) {
      this.listeners[key.name].forEach((element) => {
        element();
      });
    }
  }

  public on(event: string, callback: Function) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }
}