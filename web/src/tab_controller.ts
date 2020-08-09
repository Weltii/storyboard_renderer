import { KeyHandler } from "./key_handler";

export class TabController {
  currentLinkObject: any = null;
  tabContents: any = {};
  tabLinks: any = {};

  constructor() {
    // search for all tab-contents
    document
      .querySelectorAll("#editor-area .tab-content")
      .forEach((content) => {
        this.tabContents[content.id] = content;
      });

    // search for all tab-links and combine them with the tab-content
    document
      .querySelectorAll("#editor-area .tab-bar .tab-link")
      .forEach((link) => {
        let linkedObject = this.tabContents[link.getAttribute("link")];
        let linkObj = {
          source: link,
          linkedTo: linkedObject,
        };
        this.tabLinks[link.id] = linkObj;
        link.addEventListener("click", () => {
          this.handleLinkObjectClick(linkObj);
        });
      });

    // click on the first tab with setted linkedTo property
    for (let elementName in this.tabLinks) {
      let element = this.tabLinks[elementName];
      if (element.linkedTo) {
        element.source.click();
        return;
      }
    }
  }

  handleLinkObjectClick(linkObject) {
    if (linkObject.linkedTo) {
      if (this.currentLinkObject) {
        this.hideTab(this.currentLinkObject.linkedTo);
        (this.currentLinkObject.source as HTMLElement).classList.remove(
          "active"
        );
      }
      this.showTab(linkObject.linkedTo);
      (linkObject.source as HTMLElement).classList.add("active");
      this.currentLinkObject = linkObject;
    }
  }

  hideTab(tab) {
    if (tab) {
      tab.style.display = "none";
    }
  }

  showTab(tab) {
    if (tab) {
      tab.style.display = "block";
    }
  }
}
