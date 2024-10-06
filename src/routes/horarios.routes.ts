import { Router } from "express";
import {
  getAllHorarios,
  createHorario,
  getHorarioById,
  updateHorario,
  deleteHorario,
} from "../controllers/horarios.controller";

const router = Router();

router.get("/", getAllHorarios);
router.post("/", createHorario);
router.get("/:id", getHorarioById);
router.put("/:id", updateHorario);
router.delete("/:id", deleteHorario);

export default router;
