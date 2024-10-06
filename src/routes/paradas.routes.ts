import { Router } from "express";
import {
  getAllParadas,
  createParada,
  getParadaById,
  updateParada,
  deleteParada,
} from "../controllers/paradas.controller";

const router = Router();

router.get("/", getAllParadas);
router.post("/", createParada);
router.get("/:id", getParadaById);
router.put("/:id", updateParada);
router.delete("/:id", deleteParada);

export default router;
