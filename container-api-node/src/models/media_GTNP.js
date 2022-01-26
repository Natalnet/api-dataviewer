const mongoose = require("../database");

const media_GTNP = mongoose.model("media_GTNP", new mongoose.Schema({
  _id: String,
  user: String,
  registration: String,
  studentMediaTests: Number,
  id_class: String
}));

module.exports = media_GTNP;