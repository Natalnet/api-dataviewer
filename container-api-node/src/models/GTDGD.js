const mongoose = require("../database");

const GTDGD = mongoose.model("GTDGD", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  difficulty: Number,
  differentDaysList: Number,
  id_class: String

}));

module.exports = GTDGD;