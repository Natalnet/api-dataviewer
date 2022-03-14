const ListClassesService = require("../services/ListClassesService");

class ListClassesController {
  async handle(req, res) {
    const { id_teacher } = req.params;
    const classes = await ListClassesService.execute(id_teacher);
    return res.json(classes);
  }
}

module.exports =  new ListClassesController;