class LoginClientController {

  handle(req, res) {

    // recebe token
    const { token } = req.body;

    // colocar token nos cookies
    res.cookie("session-token", token);

    // resposta do servidor
    return res.status(200).json({
      status: "Token's already generated"
    });
    
  }

}

module.exports = new LoginClientController;