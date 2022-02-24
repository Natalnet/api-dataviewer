const mongoose = require("../database");

const User = mongoose.model("user", new mongoose.Schema({
  _id: String,
  email: String,
  name: String
}));

module.exports = User;