const { Router } = require("express");

const graphs = require("../graphs.routes");
const users = require("../users.routes");

const router = Router();

router.use("/users", users);
router.use("/graphs", graphs);

module.exports = router;