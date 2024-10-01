import type { Request, Response } from "express";

export function createParadaRota(req: Request, res: Response) {
  res.json({ message: "created" });
}

export function getParadaRota(req: Request, res: Response) {
  res.json({ message: "getted" });
}

export function updateParadaRota(req: Request, res: Response) {
  res.json({ message: "updated" });
}

export function deleteParadaRota(req: Request, res: Response) {
  res.json({ message: "deleted" });
}
