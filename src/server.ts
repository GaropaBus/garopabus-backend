import app from "./app";
import dotenv from "dotenv";

dotenv.config();

// Verificar se está em produção ou desenvolvimento
const isProduction = process.env.NODE_ENV === "production";

// Definir a porta com base no ambiente
const PORT = isProduction ? 8022 : (process.env.PORT || 8080);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});