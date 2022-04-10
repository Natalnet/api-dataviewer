const mongoose = require("mongoose");

mongoose.connect(`mongodb://mongo:27017/apinode`).then(conn => {
  console.log("[ OK ] DB Connection")
});

module.exports = mongoose;