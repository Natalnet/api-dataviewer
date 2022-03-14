const { Router } = require("express");

const ListClassesController = require("../controllers/ListClassesController");

const classes = Router();

classes.get("/:id_teacher", ListClassesController.handle);

module.exports = classes;