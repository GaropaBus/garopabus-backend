import express from "express";
import cors from "cors";

import paradasRoutes from "./routes/paradas.routes";
import rotasBairrosRoutes from "./routes/rotasBairros.routes";
import horariosRoutes from "./routes/horarios.routes";

const app = express();

app.use(express.json());
app.use(cors());

app.use("/paradas", paradasRoutes);
app.use("/rotas-bairros", rotasBairrosRoutes);
app.use("/horarios", horariosRoutes);

export default app;
