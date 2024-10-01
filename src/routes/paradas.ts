import { Router } from "express";
import {
  createParada,
  getParada,
  updateParada,
  deleteParada,
} from "../controllers/paradas";

const router = Router();

router.post("/", createParada);
router.get("/", getParada);
router.put("/", updateParada);
router.delete("/", deleteParada);

export default router;
