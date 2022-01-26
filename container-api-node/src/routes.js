const { Router } = require("express");
const ListGraphsController = require("./controllers/ListGraphsController");

const router = Router();

router.get("/graphs/:id_class", ListGraphsController.handle);

module.exports = router;