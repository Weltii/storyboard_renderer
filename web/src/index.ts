"use strict";

import "./style.scss";
import { ChuckNorrisWorker } from "./chuck_norris_service";
import { TabController } from "./tab_controller";
import { AceBrdige } from "./ace_bridge";
import { SideNav } from "./side_nav";
import { OverlayMenu } from "./overlay_menu";
import { ProjectManager } from "./project_manager";

new ChuckNorrisWorker();
new TabController();
new AceBrdige("json-editor");
new SideNav(
  document.querySelector("#left-side-nav"),
  document.querySelector("#open-side-nav")
);
new OverlayMenu(document.querySelector("#overlay-menu"));
new ProjectManager(document.querySelector('#project-manager'));