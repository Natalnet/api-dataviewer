const FetchClassesService = require("../services/FetchClassesService");

class FetchClassesController {
  async handle(req, res) {
    const { id } = req.params;
    const classes = await FetchClassesService.execute(id);
    return res.json(classes);
  }
}

module.exports =  new FetchClassesController;