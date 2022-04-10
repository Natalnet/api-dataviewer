const mongoose = require("../../database");

const GTAL = mongoose.model("GTAL", new mongoose.Schema({
  _id: String,
  more: Number,
  subject: String,
  difficulty: String,
  less: Number, 
  missing: Number,
  id_class: String
}));

module.exports = GTAL;