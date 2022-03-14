const Classes = require("../models/Classes");

class ListClassesService {
  async execute(id_teacher) {

    const classes = await Classes.find({
      id_teacher
    });

    if (classes.length === 0) {
      throw new Error("No data");
    }

    return classes;

  }
}

module.exports = new ListClassesService;