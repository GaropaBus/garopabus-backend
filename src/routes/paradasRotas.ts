import { Router } from "express";
import {
  createParadaRota,
  getParadaRota,
  updateParadaRota,
  deleteParadaRota,
} from "../controllers/paradasRotas";

const router = Router();

router.post("/", createParadaRota);
router.get("/", getParadaRota);
router.put("/", updateParadaRota);
router.delete("/", deleteParadaRota);

export default router;
