const { Router } = require("express");
const classes = require("../classes.routes");

const graphs = require("../graphs.routes");
const users = require("../users.routes");

const router = Router();

router.use("/users", users);
router.use("/graphs", graphs);
router.use("/classes", classes);

module.exports = router;