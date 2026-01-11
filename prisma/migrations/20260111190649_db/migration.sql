/*
  Warnings:

  - A unique constraint covering the columns `[CodAsesor]` on the table `Asesor` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "Asesor_CodAsesor_key" ON "Asesor"("CodAsesor");
