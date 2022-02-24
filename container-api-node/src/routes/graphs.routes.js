const { Router } = require("express");

const ListGraphsController = require("../controllers/ListGraphsController");
const ensureTokenIntegrity = require("../middlewares/ensureTokenIntegrity");

const graphs = Router();

graphs.get("/:id_class", ensureTokenIntegrity, ListGraphsController.handle);

module.exports = graphs;