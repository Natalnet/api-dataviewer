const mongoose = require("../database");

const media_GEDL = mongoose.model("media_GEDL", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  studentMediaDifficulties: Number,
  id_class: String
}));

module.exports = media_GEDL;