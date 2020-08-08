"use strict";

import "./style.scss";
import { ChuckNorrisWorker } from "./chuck_norris_service";
import { TabController } from "./tab_controller";

new ChuckNorrisWorker();
new TabController();
