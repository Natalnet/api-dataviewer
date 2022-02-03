const mongoose = require("../database");

const MediaGEAL = mongoose.model("media_GEAL", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  studentMediaSubject: Number,
  id_class: String
}));

module.exports = MediaGEAL;