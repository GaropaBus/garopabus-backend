import { Request, Response } from "express";
import prisma from "../services/prisma.service";

export const getAllParadas = async (
  req: Request,
  res: Response
): Promise<void> => {
  const paradas = await prisma.paradas.findMany();
  res.json(paradas);
};

export const createParada = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { latitude, longitude } = req.body;
  const newParada = await prisma.paradas.create({
    data: { latitude, longitude },
  });
  res.status(201).json(newParada);
};

export const getParadaById = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { id } = req.params;
  const parada = await prisma.paradas.findUnique({
    where: { ID_parada: parseInt(id) },
  });
  res.json(parada);
};

export const updateParada = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { id } = req.params;
  const { latitude, longitude } = req.body;
  const updatedParada = await prisma.paradas.update({
    where: { ID_parada: parseInt(id) },
    data: { latitude, longitude },
  });
  res.json(updatedParada);
};

export const deleteParada = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { id } = req.params;
  await prisma.paradas.delete({ where: { ID_parada: parseInt(id) } });
  res.status(204).send();
};
