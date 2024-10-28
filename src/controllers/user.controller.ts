import { Request, Response } from "express";
import prisma from "../services/prisma.service";
import bcrypt from "bcrypt";
import { CustomRequest, generateToken } from "../services/jwt.service";

const SALT_ROUNDS = 10;

export const createUser = async (
  req: Request,
  res: Response
): Promise<void> => {
  const { username, password } = req.body;

  try {
    const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);

    await prisma.user.create({
      data: { username, password: hashedPassword },
    });
    res.status(201).json("User created.");
  } catch (error) {
    console.error("Erro ao criar usuário:", error);
    res.status(500).json({ error: "Erro ao criar usuário." });
  }
};

export const loginUser = async (req: Request, res: Response): Promise<void> => {
  const { username, password } = req.body;

  if (!username || !password) {
    res.status(400).json({ error: "Username e senha são obrigatórios." });
    return;
  }

  try {
    const user = await prisma.user.findUnique({ where: { username } });

    if (user && (await bcrypt.compare(password, user.password))) {
      const token = generateToken(user.id);
      res.status(200).json({ token });
    } else {
      res.status(401).json({ error: "Credenciais inválidas." });
    }
  } catch (error) {
    console.error("Erro ao fazer login:", error);
    res.status(500).json({ error: "Erro interno ao fazer login." });
  }
};

export const getUser = async (
  req: CustomRequest,
  res: Response
): Promise<void> => {
  const { userId } = req;

  if (!userId) {
    res.status(400).json({ error: "userId não encontrado no request." });
    return;
  }

  try {
    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: { id: true, username: true },
    });

    if (user) {
      res.status(200).json(user);
    } else {
      res.status(404).json({ error: "Usuário não encontrado." });
    }
  } catch (error) {
    console.error("Erro ao buscar usuário:", error);
    res.status(500).json({ error: "Erro ao buscar usuário." });
  }
};
