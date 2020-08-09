export class OverlayMenu {
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
  }

  onSaveButtonClick() {
    // Todo add logic!
    console.warn("onSaveButtonClick is currently not implemented!");
  }

  onRenderButtonClick() {
    // Todo add logic!
    console.warn("onRenderButtonClick is currently not implemented!");
  }

  onLayoutSelectionChange(event: Event) {
    //@ts-ignore
    const value = event.target.value;
    this.setLayout(value);
  }

  private fillLayoutSelection() {
    const layouts = ["EASY_LAYOUT", "MOVIE_LAYOUT"];
    layouts.forEach((layout: string) => {
      let option: HTMLOptionElement = document.createElement("option");
      option.value = layout;
      option.innerText = layout.replace("_", " ");
      this.layoutSelection.appendChild(option);

      if (!this.currentLayout) {
        this.setLayout(layout);
      }
    });
  }

  private setLayout(layout: string) {
    this.currentLayout = layout;
  }
}
