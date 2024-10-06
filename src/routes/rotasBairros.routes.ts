import { Router } from "express";
import {
  getAllRotas,
  createRota,
  getRotaById,
  updateRota,
  deleteRota,
} from "../controllers/rotasBairros.controller";

const router = Router();

router.get("/", getAllRotas);
router.post("/", createRota);
router.get("/:id", getRotaById);
router.put("/:id", updateRota);
router.delete("/:id", deleteRota);

export default router;
