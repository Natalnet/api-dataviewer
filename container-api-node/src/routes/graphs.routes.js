const { Router } = require("express");

const ListGraphsController = require("../controllers/ListGraphsController");

const graphs = Router();

graphs.get("/:id_class", ListGraphsController.handle);

module.exports = graphs;