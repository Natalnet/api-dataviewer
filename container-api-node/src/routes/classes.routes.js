const { Router } = require("express");
const FetchClassesController = require("../controllers/FetchClassesController");
const ensureTokenIntegrity = require("../middlewares/ensureTokenIntegrity");

const classes = Router();

classes.get("/:id_teacher", ensureTokenIntegrity, FetchClassesController.handle);

module.exports = classes;