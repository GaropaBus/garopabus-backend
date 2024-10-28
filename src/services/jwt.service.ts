import type { Request, Response } from "express";
import { NextFunction } from "express";
import jwt from "jsonwebtoken";

export const generateToken = (userId: number) => {
  return jwt.sign({ userId }, process.env.JWT_SECRET as string, {
    expiresIn: "1d",
  });
};

export const authenticateToken = (
  req: CustomRequest,
  res: Response,
  next: NextFunction
): void => {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];

  if (!token) {
    res.sendStatus(401);
    return;
  }

  jwt.verify(token, process.env.JWT_SECRET as string, (err, decoded: any) => {
    if (err) return res.sendStatus(403);
    req.userId = decoded.userId;
    next();
  });
};

export interface CustomRequest extends Request {
  userId?: number;
}
