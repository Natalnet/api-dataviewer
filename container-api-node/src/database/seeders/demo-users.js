const User = require("../../models/User")

const data = [
  {
    _id: "91f5167c34c400758115c2a6826ec2e3",
    name: "Professor Administrador",
    email: "dataviewer.platform@gmail.com"
  },
]

// remove existing data
User.deleteMany({})
  .then(() => {
    console.log("[ OK ] Users docs were deleted")
    // insert data
    User.insertMany(data)
      .then(() => {
        console.log("[ OK ] Users seed inserted")
      })
  })


