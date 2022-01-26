const GENL = require("../models/GENL");
const GENP = require("../models/GENP");
const GTDL = require("../models/GTDL");
const GTDP = require("../models/GTDP");
const GTAL = require("../models/GTAL");
const GTAP = require("../models/GTAP");
const GTNL = require("../models/GTNL");
const GTNP = require("../models/GTNP");
const GEDL = require("../models/GEDL");
const GEDP = require("../models/GEDP");
const GEAL = require("../models/GEAL");
const GEAP = require("../models/GEAP");

const media_GTNL = require("../models/media_GTNL");
const media_GTNP = require("../models/media_GTNP");
const media_GEDL = require("../models/media_GEDL");
const media_GEDP = require("../models/media_GEDP");
const media_GEAL = require("../models/media_GEAL");
const media_GEAP = require("../models/media_GEAP");

const GTDGL = require("../models/GTDGL");
const GTDGA = require("../models/GTDGA");
const GTDGD = require("../models/GTDGD");

const GTTMQQMDD = require("../models/GTTMQQMDD");
const GTTMDDL = require("../models/GTTMDDL");
const GATGQTDD = require("../models/GATGQTDD");
const GTTGQSQ = require("../models/GTTGQSQ");

class ListGraphsController {
  async handle(request, response) {

    const { id_class } = request.params;

    const data = {
      "GENL": await GENL.find({ id_class }),
      "GENP": await GENP.find({ id_class }),
      "GTDL": await GTDL.find({ id_class }),
      "GTDP": await GTDP.find({ id_class }),
      "GTAL": await GTAL.find({ id_class }),
      "GTAP": await GTAP.find({ id_class }),
      "GTNL": await GTNL.find({ id_class }),
      "GTNP": await GTNP.find({ id_class }),
      "GEDL": await GEDL.find({ id_class }),
      "GEDP": await GEDP.find({ id_class }),
      "GEAL": await GEAL.find({ id_class }),
      "GEAP": await GEAP.find({ id_class }),
      "media_GTNL": await media_GTNL.find({ id_class }),
      "media_GTNP": await media_GTNP.find({ id_class }),
      "media_GEDL": await media_GEDL.find({ id_class }),
      "media_GEDP": await media_GEDP.find({ id_class }),
      "media_GEAL": await media_GEAL.find({ id_class }),
      "media_GEAP": await media_GEAP.find({ id_class }),
      "GTDGL": await GTDGL.find({ id_class }),
      "GTDGA": await GTDGA.find({ id_class }),
      "GTDGD": await GTDGD.find({ id_class }),
      "GTTMQQMDD": await GTTMQQMDD.find({ id_class }),
      "GTTMDDL": await GTTMDDL.find(),
      "GATGQTDD": await GATGQTDD.find({ id_class }),
      "GTTGQSQ": await GTTGQSQ.find()
    };

    return response.json(data);
  }
}

module.exports = new ListGraphsController;