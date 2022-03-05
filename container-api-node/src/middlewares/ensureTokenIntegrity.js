const { OAuth2Client } = require("google-auth-library");

const ensureTokenIntegrity = async (req, res, next) => {

  // recuperar token do Header da requisição
  const string = req.headers["authorization"];

  if (!string) {
    throw new Error("No token was added. Please sign in.");
  }

  const [bearer, authtoken] = string.split(" ");
  const token = authtoken;

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