import { Router } from "express";
import {
  getAllRotas,
  createRota,
  getRotaById,
  updateRota,
  deleteRota,
} from "../controllers/rotasBairros.controller";
import { authenticateToken } from "../services/jwt.service";

const router = Router();

router.get("/", getAllRotas);
router.post("/", authenticateToken, createRota);
router.get("/:id", getRotaById);
router.put("/:id", authenticateToken, updateRota);
router.delete("/:id", authenticateToken, deleteRota);

export default router;
