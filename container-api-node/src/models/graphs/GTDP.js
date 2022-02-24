const mongoose = require("../../database");

const GTDP = mongoose.model("GTDP", new mongoose.Schema({
  _id: String,
  more: Number,
  difficulty: String,
  less: Number,
  missing: Number,
  id_class: String

}));

module.exports = GTDP;