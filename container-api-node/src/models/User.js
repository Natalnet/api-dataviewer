const mongoose = require("../database");

const User = mongoose.model("User", new mongoose.Schema({
  _id: String,
  email: String
}));

module.exports = User;