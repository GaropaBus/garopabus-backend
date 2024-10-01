import { Router } from "express";
import {
  createRota,
  getRota,
  updateRota,
  deleteRota,
} from "../controllers/rotas";

const router = Router();

router.post("/", createRota);
router.get("/", getRota);
router.put("/", updateRota);
router.delete("/", deleteRota);

export default router;
