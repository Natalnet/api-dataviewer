const { Router } = require("express");

const ListClassesController = require("../controllers/ListClassesController");
const ensureTokenIntegrity = require("../middlewares/ensureTokenIntegrity");

const classes = Router();

classes.get("/:id_teacher", ensureTokenIntegrity, ListClassesController.handle);

module.exports = classes;