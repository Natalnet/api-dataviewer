const User = require("../models/User");

class AuthenticateUserService {

  async execute(email) {

    const allowedDomains = ["ufrn.edu.br", "ufrn.br", "ect.ufrn.br", "gmail.com"];
    const [prefix, domain] = email.split("@");

    if (!allowedDomains.includes(domain)) {
      throw new Error("Email domain isn't valid");
    }

    const user = await User.find({
      email: email
    });

    if (!user) {
      throw new Error("Email isn't on whitelist");
    }

    return user;

  }

}

module.exports = new AuthenticateUserService;