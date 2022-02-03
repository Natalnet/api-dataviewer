// o usuário é realmente do lop?

const AuthenticateUserService = require("../services/AuthenticateUserService");

class AuthenticateUserController {

  async handle(req, res) {

    const { email } = req.body;

    const user = await AuthenticateUserService.execute(email);

    return res.status(200).json(user);
    
  }

}

module.exports = new AuthenticateUserController;
