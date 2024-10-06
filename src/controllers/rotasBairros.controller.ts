import { Request, Response } from "express";
import prisma from "../services/prisma.service";

export const getAllRotas = async (
  req: Request,
  res: Response
): Promise<void> => {
  const rotas = await prisma.rotasBairros.findMany();
  res.json(rotas);
};

export const createRota = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { local_inicio, local_final } = req.body;
  const newRota = await prisma.rotasBairros.create({
    data: { local_inicio, local_final },
  });
  res.status(201).json(newRota);
};

export const getRotaById = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { id } = req.params;
  const rota = await prisma.rotasBairros.findUnique({
    where: { ID_rota_bairro: parseInt(id) },
  });
  res.json(rota);
};

export const updateRota = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { id } = req.params;
  const { local_inicio, local_final } = req.body;
  const updatedRota = await prisma.rotasBairros.update({
    where: { ID_rota_bairro: parseInt(id) },
    data: { local_inicio, local_final },
  });
  res.json(updatedRota);
};

export const deleteRota = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { id } = req.params;
  await prisma.rotasBairros.delete({ where: { ID_rota_bairro: parseInt(id) } });
  res.status(204).send();
};
