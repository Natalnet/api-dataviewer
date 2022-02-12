const User = require("../models/User");

class FetchUserService {
  async execute(id) {

    const user = await User.findById(id);

    // verificar se ID existe
    if (!user) {
      throw new Error("Ivalid identifier");
    }

    // retorne usuario
    return user;

  }
}

module.exports = new FetchUserService;