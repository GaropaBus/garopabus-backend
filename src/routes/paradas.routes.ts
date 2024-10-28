import { Router } from "express";
import {
  getAllParadas,
  createParada,
  getParadaById,
  updateParada,
  deleteParada,
} from "../controllers/paradas.controller";
import { authenticateToken } from "../services/jwt.service";

const router = Router();

router.get("/", getAllParadas);
router.post("/", authenticateToken, createParada);
router.get("/:id", getParadaById);
router.put("/:id", authenticateToken, updateParada);
router.delete("/:id", authenticateToken, deleteParada);

export default router;
