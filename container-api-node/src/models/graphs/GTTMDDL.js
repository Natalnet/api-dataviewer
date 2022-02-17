const mongoose = require("../../database");

const GTTMDDL = mongoose.model("GTTMDDL", new mongoose.Schema({
  _id: String,
  list: String,
  question: String,
  maxTime: Number,
  maxDifferentDays: Number,
  id_class: String
}));

module.exports = GTTMDDL;