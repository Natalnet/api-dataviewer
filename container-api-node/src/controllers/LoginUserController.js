class LoginUserController {

  async handle(req, res) {
    res.render("login"); 
  }
  
}

module.exports = new LoginUserController;