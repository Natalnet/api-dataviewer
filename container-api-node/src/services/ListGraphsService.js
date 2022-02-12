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
const GTDGL = require("../models/GTDGL");
const GTDGA = require("../models/GTDGA");
const GTDGD = require("../models/GTDGD");
const GTTMQQMDD = require("../models/GTTMQQMDD");
const GTTMDDL = require("../models/GTTMDDL");
const GATGQTDD = require("../models/GATGQTDD");
const GTTGQSQ = require("../models/GTTGQSQ");

const MediaGTNL = require("../models/MediaGTNL");
const MediaGTNP = require("../models/MediaGTNP");
const MediaGEDL = require("../models/MediaGEDL");
const MediaGEDP = require("../models/MediaGEDP");
const MediaGEAL = require("../models/MediaGEAL");
const MediaGEAP = require("../models/MediaGEAP");

class ListGraphsService {

  async execute(id_class) {

    // montagem dos dados
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
      "media_GTNL": await MediaGTNL.find({ id_class }),
      "media_GTNP": await MediaGTNP.find({ id_class }),
      "media_GEDL": await MediaGEDL.find({ id_class }),
      "media_GEDP": await MediaGEDP.find({ id_class }),
      "media_GEAL": await MediaGEAL.find({ id_class }),
      "media_GEAP": await MediaGEAP.find({ id_class }),
      "GTDGL": await GTDGL.find({ id_class }),
      "GTDGA": await GTDGA.find({ id_class }),
      "GTDGD": await GTDGD.find({ id_class }),
      "GTTMQQMDD": await GTTMQQMDD.find({ id_class }),
      "GTTMDDL": await GTTMDDL.find({ id_class }),
      "GATGQTDD": await GATGQTDD.find({ id_class }),
      "GTTGQSQ": await GTTGQSQ.find({ id_class })
    };

    // recuperar chaves do objeto e a quantidade delas
    const keys = Object.keys(data);
    const n = keys.length;

    // filtrar dados vazios
    const empties = keys.filter(key => data[key].length === 0);

    // verificar se id não existe: o vetor de dados vazios tem tamanho n
    if (empties.length === n) {
      throw new Error("Invalid identifier or no data");
    }

    return data;
  }

}

module.exports = new ListGraphsService;