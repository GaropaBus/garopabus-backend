import type { Request, Response } from "express";

export function createRota(req: Request, res: Response) {
  res.json({ message: "created" });
}

export function getRota(req: Request, res: Response) {
  res.json({ message: "getted" });
}

export function updateRota(req: Request, res: Response) {
  res.json({ message: "updated" });
}

export function deleteRota(req: Request, res: Response) {
  res.json({ message: "deleted" });
}
