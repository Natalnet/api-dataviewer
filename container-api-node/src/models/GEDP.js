const mongoose = require("../database");

const GEDP = mongoose.model("GEDP", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  difficulty: String,
  mediaDifficulty: Number,
  mediaDifficultyClass: Number,
  id_class: String
}));

module.exports = GEDP;