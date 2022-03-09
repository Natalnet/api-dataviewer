const { Router } = require("express");

const classes = require("./classes.routes");
const graphs = require("./graphs.routes");
const users = require("./users.routes");

const router = Router();

// Resources
router.use("/users", users);
router.use("/graphs", graphs);
router.use("/classes", classes);

// Alias para a rota de login
router.get("/", (req, res) => { res.redirect("/users/login"); })

module.exports = router;