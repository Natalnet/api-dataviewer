const mongoose = require("../database");

const GTDL = mongoose.model("GTDL", new mongoose.Schema({
  _id: String,
  more: Number,
  difficulty: String,
  less: Number,
  missing: Number,
  id_class: String
}));

module.exports = GTDL;