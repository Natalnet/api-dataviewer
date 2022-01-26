const mongoose = require("../database");

const media_GEAP = mongoose.model("media_GEAP", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  studentMediaSubject: Number,
  id_class: String
}));

module.exports = media_GEAP;