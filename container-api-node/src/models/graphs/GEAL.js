const mongoose = require("../../database");


const GEAL = mongoose.model("GEAL", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  subject: String,
  mediaSubject: Number,
  mediaSubjectClass: Number,
  id_class: String
}));

module.exports = GEAL;