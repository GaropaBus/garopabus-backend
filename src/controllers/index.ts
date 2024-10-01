import type { Request, Response } from "express";

export function getIndex(req: Request, res: Response) {
  res.json({ message: "Online!" });
}
