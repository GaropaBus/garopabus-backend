import type { Request, Response } from "express";

export function createParada(req: Request, res: Response) {
  res.json({ message: "created" });
}

export function getParada(req: Request, res: Response) {
  res.json({ message: "getted" });
}

export function updateParada(req: Request, res: Response) {
  res.json({ message: "updated" });
}

export function deleteParada(req: Request, res: Response) {
  res.json({ message: "deleted" });
}
