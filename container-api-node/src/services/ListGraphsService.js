const GENL = require("../models/graphs/GENL");
const GENP = require("../models/graphs/GENP");
const GTDL = require("../models/graphs/GTDL");
const GTDP = require("../models/graphs/GTDP");
const GTAL = require("../models/graphs/GTAL");
const GTAP = require("../models/graphs/GTAP");
const GTNL = require("../models/graphs/GTNL");
const GTNP = require("../models/graphs/GTNP");
const GEDL = require("../models/graphs/GEDL");
const GEDP = require("../models/graphs/GEDP");
const GEAL = require("../models/graphs/GEAL");
const GEAP = require("../models/graphs/GEAP");
const GTDGL = require("../models/graphs/GTDGL");
const GTDGA = require("../models/graphs/GTDGA");
const GTDGD = require("../models/graphs/GTDGD");
const GTTMQQMDD = require("../models/graphs/GTTMQQMDD");
const GTTMDDL = require("../models/graphs/GTTMDDL");
const GATGQTDD = require("../models/graphs/GATGQTDD");
const GTTGQSQ = require("../models/graphs/GTTGQSQ");

const MediaGTNL = require("../models/graphs/MediaGTNL");
const MediaGTNP = require("../models/graphs/MediaGTNP");
const MediaGEDL = require("../models/graphs/MediaGEDL");
const MediaGEDP = require("../models/graphs/MediaGEDP");
const MediaGEAL = require("../models/graphs/MediaGEAL");
const MediaGEAP = require("../models/graphs/MediaGEAP");

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

    // verificar se id_class não existe: o vetor de dados vazios tem tamanho n
    if (empties.length === n) {
      // precisa ter um model Classes para verificar se o id_class existe
      throw new Error("No data or invalid identifier");
    }

    return data;
  }

}

module.exports = new ListGraphsService;