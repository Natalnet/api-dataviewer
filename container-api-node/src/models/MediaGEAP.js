const mongoose = require("../database");

const MediaGEAP = mongoose.model("media_GEAP", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  studentMediaSubject: Number,
  id_class: String
}));

module.exports = MediaGEAP;