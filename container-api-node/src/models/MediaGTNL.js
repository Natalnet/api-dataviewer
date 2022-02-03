const mongoose = require("../database");

const MediaGTNL = mongoose.model("media_GTNL", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  studentMediaLists: Number,
  id_class: String
}));

module.exports = MediaGTNL;