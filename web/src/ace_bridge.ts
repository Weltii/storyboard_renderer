import * as ace from "brace";
import "brace/mode/javascript";
import "brace/theme/monokai";
import { KeyHandler } from "./key_handler";

export class AceBrdige {
  editor: any;
  keyHandler: KeyHandler;

  constructor(htmlElementName: string) {
    this.keyHandler = KeyHandler.getInstance();
    this.editor = ace.edit(htmlElementName);
    this.editor.getSession().setMode("ace/mode/javascript");
    this.editor.setTheme("ace/theme/monokai");

    this.setText(
      JSON.stringify(
        {
          info: "To edit something, you must load a project!",
          "info#2": "In the pdf-viewer you can see a example storyboard",
        },
        null,
        "\t"
      )
    );

    this.keyHandler.on("ctrl_save", this.saveSession.bind(this));
  }

  setText(text: string) {
    this.editor.getSession().setValue(text);
  }

  saveSession(): void {
    console.log("Save ace session!");
    // TODO do something ;)
  }
}
