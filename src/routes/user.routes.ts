import { Router } from "express";
import { createUser, loginUser, getUser } from "../controllers/user.controller";
import { authenticateToken } from "../services/jwt.service";

const router = Router();

router.post("/create", authenticateToken, createUser);
router.post("/login", loginUser);
router.get("/getuser", authenticateToken, getUser);

export default router;
