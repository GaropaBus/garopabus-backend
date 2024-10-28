import { Router } from "express";
import {
  getAllHorarios,
  createHorario,
  getHorarioById,
  updateHorario,
  deleteHorario,
} from "../controllers/horarios.controller";
import { authenticateToken } from "../services/jwt.service";

const router = Router();

router.get("/", getAllHorarios);
router.post("/", authenticateToken, createHorario);
router.get("/:id", getHorarioById);
router.put("/:id", authenticateToken, updateHorario);
router.delete("/:id", authenticateToken, deleteHorario);

export default router;
