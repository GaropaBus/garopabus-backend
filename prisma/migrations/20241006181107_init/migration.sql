-- CreateTable
CREATE TABLE "Paradas" (
    "ID_parada" SERIAL NOT NULL,
    "latitude" DECIMAL(10,8) NOT NULL,
    "longitude" DECIMAL(11,8) NOT NULL,

    CONSTRAINT "Paradas_pkey" PRIMARY KEY ("ID_parada")
);

-- CreateTable
CREATE TABLE "RotasBairros" (
    "ID_rota_bairro" SERIAL NOT NULL,
    "local_inicio" VARCHAR(100) NOT NULL,
    "local_final" VARCHAR(100) NOT NULL,

    CONSTRAINT "RotasBairros_pkey" PRIMARY KEY ("ID_rota_bairro")
);

-- CreateTable
CREATE TABLE "ParadasRotas" (
    "ID_parada" INTEGER NOT NULL,
    "ID_rota_bairro" INTEGER NOT NULL,

    CONSTRAINT "ParadasRotas_pkey" PRIMARY KEY ("ID_parada","ID_rota_bairro")
);

-- CreateTable
CREATE TABLE "Horarios" (
    "ID_horario" SERIAL NOT NULL,
    "ID_rota_bairro" INTEGER NOT NULL,
    "hora" TIME NOT NULL,
    "tipo" VARCHAR(10) NOT NULL,

    CONSTRAINT "Horarios_pkey" PRIMARY KEY ("ID_horario")
);

-- AddForeignKey
ALTER TABLE "ParadasRotas" ADD CONSTRAINT "ParadasRotas_ID_parada_fkey" FOREIGN KEY ("ID_parada") REFERENCES "Paradas"("ID_parada") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ParadasRotas" ADD CONSTRAINT "ParadasRotas_ID_rota_bairro_fkey" FOREIGN KEY ("ID_rota_bairro") REFERENCES "RotasBairros"("ID_rota_bairro") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Horarios" ADD CONSTRAINT "Horarios_ID_rota_bairro_fkey" FOREIGN KEY ("ID_rota_bairro") REFERENCES "RotasBairros"("ID_rota_bairro") ON DELETE RESTRICT ON UPDATE CASCADE;
