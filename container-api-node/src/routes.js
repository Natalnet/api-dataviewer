const { Router } = require("express");

const ListGraphsController = require("./controllers/ListGraphsController");
const LoginController = require("./controllers/LoginController");
const ensureTokenIntegrity = require("./middlewares/ensureTokenIntegrity");

const router = Router();

// view de login
router.get("/login", (req, res) => { res.render("login"); });
router.post("/login", LoginController.handle);

// rotas secretas
router.get("/graphs/:id_class", ensureTokenIntegrity, ListGraphsController.handle);

module.exports = router;