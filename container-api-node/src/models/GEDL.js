const mongoose = require("../database");

const GEDL = mongoose.model("GEDL", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  difficulty: String,
  mediaDifficulty: Number,
  mediaDifficultyClass: Number,
  id_class: String
}));

module.exports = GEDL;