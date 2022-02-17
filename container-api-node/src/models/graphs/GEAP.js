const mongoose = require("../../database");


const GEAP = mongoose.model("GEAP", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  subject: String,
  mediaSubject: Number,
  mediaSubjectClass: Number,
  id_class: String
}));

module.exports = GEAP;