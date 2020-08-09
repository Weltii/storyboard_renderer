"use strict";

import "./style.scss";
import { ChuckNorrisWorker } from "./chuck_norris_service";
import { TabController } from "./tab_controller";
import { AceBrdige } from "./ace_bridge";

new ChuckNorrisWorker();
new TabController();
new AceBrdige("json-editor");
