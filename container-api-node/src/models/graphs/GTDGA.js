const mongoose = require("../../database");

const GTDGA = mongoose.model("GTDGA", new mongoose.Schema({
  _id: String,
  id_class: String
}));

module.exports = GTDGA;