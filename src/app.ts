import express from "express";
import cors from "cors";

import indexRoutes from "./routes/index";
import paradasRoutes from "./routes/paradas";
import horariosRoutes from "./routes/horarios";
import rotasRoutes from "./routes/rotas";

const app = express();

app.use(express.json());
app.use(cors());

app.use("/", indexRoutes);
app.use("/paradas", paradasRoutes);
app.use("/horarios", horariosRoutes);
app.use("/rotas", rotasRoutes);

export default app;
