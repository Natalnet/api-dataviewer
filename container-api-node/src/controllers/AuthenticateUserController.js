// o usuário é realmente do lop?

const AuthenticateUserService = require("../services/AuthenticateUserService");

class AuthenticateUserController {

  async handle(req, res) {

    const { email, token } = req.body;
    const user = await AuthenticateUserService.execute(email);

    // colocar token nos cookies
    res.cookie("session-token", token);

    return res.status(200).json(user);
    
  }

}

module.exports = new AuthenticateUserController;
