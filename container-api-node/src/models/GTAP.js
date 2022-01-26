const mongoose = require("../database");

const GTAP = mongoose.model("GTAP", new mongoose.Schema({
  _id: String,
  id_class: String

}));

module.exports = GTAP;