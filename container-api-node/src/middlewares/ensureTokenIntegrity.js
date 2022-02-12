const { OAuth2Client } = require("google-auth-library");

const ensureTokenIntegrity = async (req, res, next) => {

  // recuperar token dos cookies
  const token = req.cookies["APINJS_AUTH"];

  if (!token) {
    throw new Error("No token was added. Please sign in.");
  }

  // verificar integridade dele
  const CLIENT_ID = process.env.CLIENT_ID;
  const client = new OAuth2Client(CLIENT_ID);

  const ticket = await client.verifyIdToken({
    idToken: token,
    audience: CLIENT_ID
  });

  const payload = ticket.getPayload();

  if (!payload) {
    throw new Error("Token isn't valid");
  }

  return next();

}

module.exports = ensureTokenIntegrity;