const mongoose = require("../../database");

const GTNL = mongoose.model("GTNL", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  list: String,
  totalHitPercentage: Number,
  totalQuestionslist: Number,
  medialist: Number,
  id_list: String,
  shortTitle: String,
  id_class: String,
  mediaListClass: Number
}));

module.exports = GTNL;