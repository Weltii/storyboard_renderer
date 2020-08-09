export class SideNav {
  private root: HTMLElement;
  private openButton: HTMLElement;
  private closeButton: HTMLElement;

  constructor(navRoot: HTMLElement, openButton: HTMLElement) {
    this.root = navRoot;
    this.openButton = openButton;
    this.openButton.addEventListener("click", this.open.bind(this));
    this.closeButton = navRoot.querySelector(".close-button");
    this.closeButton.addEventListener("click", this.close.bind(this));
  }

  open() {
    this.root.classList.add("open");
  }

  close() {
    this.root.classList.remove("open");
  }
}
