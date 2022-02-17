const mongoose = require("../../database");

const GTTGQSQ = mongoose.model("GTTGQSQ", new mongoose.Schema({
  _id: String,
  question: String,
  quantity: Number,
  timeInSecounds: Number,
  id_class: String
}));

module.exports = GTTGQSQ;