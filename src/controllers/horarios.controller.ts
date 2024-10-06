import { Request, Response } from "express";
import prisma from "../services/prisma.service";

export const getAllHorarios = async (
  req: Request,
  res: Response
): Promise<void> => {
  const horarios = await prisma.horarios.findMany();
  res.json(horarios);
};

export const createHorario = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { ID_rota_bairro, hora, tipo } = req.body;
  const newHorario = await prisma.horarios.create({
    data: { ID_rota_bairro, hora: new Date(hora), tipo },
  });
  res.status(201).json(newHorario);
};

export const getHorarioById = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { id } = req.params;
  const horario = await prisma.horarios.findUnique({
    where: { ID_horario: parseInt(id) },
  });
  res.json(horario);
};

export const updateHorario = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { id } = req.params;
  const { ID_rota_bairro, hora, tipo } = req.body;
  const updatedHorario = await prisma.horarios.update({
    where: { ID_horario: parseInt(id) },
    data: { ID_rota_bairro, hora: new Date(hora), tipo },
  });
  res.json(updatedHorario);
};

export const deleteHorario = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { id } = req.params;
  await prisma.horarios.delete({ where: { ID_horario: parseInt(id) } });
  res.status(204).send();
};
