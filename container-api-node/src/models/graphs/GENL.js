const mongoose = require("../../database");

const GENL = mongoose.model("GENL", new mongoose.Schema({
  _id: String,
  list: String,
  shortTitle: String,
  dateList: Number,
  more: Number,
  less: Number,
  missing: Number,
  id_class: String
}));

module.exports = GENL;