require("express-async-errors");

const express = require("express");
const router = require("./routes");
const cookieParser = require('cookie-parser');
const cors = require("cors");

const { json } = require("express");

const app = express();

app.use(express.static("public"));
app.set("view engine", "ejs");

app.use(cors());
app.use(json());
app.use(cookieParser());
app.use(router);

// capturar erros
app.use((err, req, res, next) => {
  if (err instanceof Error) {
    return res.status(400).json({
      error: err.message
    })
  }
  // caso o erro não for uma instância da classe Error 
  return res.status(500).json({
    status: "error",
    message: "Internal server error"
  })
})

app.listen(process.env.APP_PORT, () => {
  console.log(`[ OK ] Server is listening on ${process.env.APP_PORT}`);
});

/* require("./database") */