const mongoose = require("../database");

const GENP = mongoose.model("GENP", new mongoose.Schema({
  _id: String,
  id_class: String

}));

module.exports = GENP;