require("express-async-errors");

const express = require("express");
const router = require("./routes");

const { json } = require("express");

const app = express();

app.use(json());

app.use(router);

app.listen(3333, () => {
  console.log(`[ OK ] Server is listening on ${3333}`);
});