import type { Request, Response } from "express";

export function createHorario(req: Request, res: Response) {
  res.json({ message: "created" });
}

export function getHorario(req: Request, res: Response) {
  res.json({ message: "getted" });
}

export function updateHorario(req: Request, res: Response) {
  res.json({ message: "updated" });
}

export function deleteHorario(req: Request, res: Response) {
  res.json({ message: "deleted" });
}
