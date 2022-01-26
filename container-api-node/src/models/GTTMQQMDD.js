const mongoose = require("../database");

const GTTMQQMDD = mongoose.model("GTTMQQMDD", new mongoose.Schema({
  _id: String,
  question: String,
  maxTime: Number,
  maxDifferentDays: Number,
  id_class: String

}));

module.exports = GTTMQQMDD;