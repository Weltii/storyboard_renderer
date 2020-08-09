"use strict";

import "./style.scss";
import { ChuckNorrisWorker } from "./chuck_norris_service";
import { TabController } from "./tab_controller";
import { AceBrdige } from "./ace_bridge";
import { SideNav } from "./side_nav";

new ChuckNorrisWorker();
new TabController();
new AceBrdige("json-editor");
new SideNav(
  document.querySelector("#left-side-nav"),
  document.querySelector("#open-side-nav")
);