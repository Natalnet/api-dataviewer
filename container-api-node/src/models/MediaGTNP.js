const mongoose = require("../database");

const MediaGTNP = mongoose.model("media_GTNP", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  studentMediaTests: Number,
  id_class: String
}));

module.exports = MediaGTNP;