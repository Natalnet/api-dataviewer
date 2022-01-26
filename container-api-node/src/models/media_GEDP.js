const mongoose = require("../database");

const media_GEDP = mongoose.model("media_GEDP", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  studentMediaDifficulties: Number,
  id_class: String
}));

module.exports = media_GEDP;