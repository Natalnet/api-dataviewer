const mongoose = require("../database");

const Classes = mongoose.model("teachers_classes", new mongoose.Schema({
  _id: String,
  author: String,
  code: String,
  createdAt: String,
  id_class: String,
  id_teacher: String,
  name_class: String,
  semester: Number,
  state: String,
  studentsCount: Number,
  teachersCount: Number,
  year: Number,
  email: String,
  name_teacher: String
}));

module.exports = Classes;