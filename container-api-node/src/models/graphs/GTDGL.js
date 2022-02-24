const mongoose = require("../../database");

const GTDGL = mongoose.model("GTDGL", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  list: String,
  differentDaysList: Number,
  id_class: String
}));

module.exports = GTDGL;