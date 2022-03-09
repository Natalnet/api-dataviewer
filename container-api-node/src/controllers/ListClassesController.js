const ListClassesService = require("../services/ListClassesService");

class ListClassesController {
  async handle(req, res) {
    const { id } = req.params;
    const classes = await ListClassesService.execute(id);
    return res.json(classes);
  }
}

module.exports =  new ListClassesController;