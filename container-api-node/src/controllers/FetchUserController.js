const FetchUserService = require("../services/FetchUserService");

class FetchUserController {
  async handle(req, res) {

    const { id } = req.params;
    const user = await FetchUserService.execute(id);

    return res.json(user);

  }
}

module.exports = new FetchUserController;