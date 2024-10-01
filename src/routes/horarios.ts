import { Router } from "express";
import {
  createHorario,
  getHorario,
  updateHorario,
  deleteHorario,
} from "../controllers/horarios";

const router = Router();

router.post("/", createHorario);
router.get("/", getHorario);
router.put("/", updateHorario);
router.delete("/", deleteHorario);

export default router;
