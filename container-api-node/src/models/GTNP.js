const mongoose = require("../database");

const GTNP = mongoose.model("GTNP", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  test: String,
  totalHitPercentage: Number,
  totalQuestionstest: Number,
  mediatest: Number,
  id_test: String,
  shortTitle: String,
  id_class: String,
  mediaTestClass: Number
}));

module.exports = GTNP;