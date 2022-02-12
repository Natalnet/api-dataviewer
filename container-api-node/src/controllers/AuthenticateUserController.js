// o usuário é realmente do lop?

const AuthenticateUserService = require("../services/AuthenticateUserService");

class AuthenticateUserController {

  async handle(req, res) {

    const { email, token } = req.body;
    const user = await AuthenticateUserService.execute(email);

    // colocar token e id do usuário nos cookies
    res.cookie("APINJS_AUTH", token);
    res.cookie("APINJS_UID", user[0]._id)

    return res.status(200).json(user);
    
  }

}

module.exports = new AuthenticateUserController;
