const mongoose = require("../database");

const GATGQTDD = mongoose.model("GATGQTDD", new mongoose.Schema({
  _id: String,
  registration: String,
  question: String,
  list: String,
  totalSecounds: Number,
  differentDays: Number,
  user: String,
  id_class: String
}));

module.exports = GATGQTDD;