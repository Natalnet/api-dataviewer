const ListGraphsService = require("../services/ListGraphsService");

class ListGraphsController {
  async handle(request, response) {

    const { id_class } = request.params;
    const data = await ListGraphsService.execute(id_class);
   
    return response.json(data);
  }
}

module.exports = new ListGraphsController;