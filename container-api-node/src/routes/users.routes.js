const { Router } = require("express");

const AuthenticateUserController = require("../controllers/AuthenticateUserController");
const FetchUserController = require("../controllers/FetchUserController");
const LoginUserController = require("../controllers/LoginUserController");

const ensureTokenIntegrity = require("../middlewares/ensureTokenIntegrity");

const users = Router();

users.get("/login", LoginUserController.handle);
users.post("/auth", AuthenticateUserController.handle);
users.get("/:id", ensureTokenIntegrity, FetchUserController.handle);

module.exports = users;