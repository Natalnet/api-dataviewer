// o usuário é realmente do lop?

const AuthenticateUserService = require("../services/AuthenticateUserService");

class AuthenticateUserController {

  async handle(req, res) {

    const { email, token } = req.body;
    const user = await AuthenticateUserService.execute(email);

    // colocar token e id do usuário nos cookies
    if (user.length != 0) {
      res.cookie("APINJS_AUTH", token);
      res.cookie("APINJS_UID", user[0]._id)
    } 
    
    else {
      // evitar que o cookie de um usuário autenticado seja usado por outro que não é
      res.clearCookie("APINJS_AUTH");
      res.clearCookie("APINJS_UID");
    }

    return res.status(200).json(user);
    
  }

}

module.exports = new AuthenticateUserController;
