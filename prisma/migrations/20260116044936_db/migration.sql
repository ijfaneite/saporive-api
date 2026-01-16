-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "username" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "hashedPassword" TEXT NOT NULL,
    "disabled" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Asesor" (
    "idAsesor" TEXT NOT NULL,
    "Asesor" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "createdBy" TEXT NOT NULL,
    "updatedBy" TEXT NOT NULL,

    CONSTRAINT "Asesor_pkey" PRIMARY KEY ("idAsesor")
);

-- CreateTable
CREATE TABLE "Producto" (
    "idProducto" TEXT NOT NULL,
    "Producto" TEXT NOT NULL,
    "Precio" DOUBLE PRECISION NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "createdBy" TEXT NOT NULL,
    "updatedBy" TEXT NOT NULL,

    CONSTRAINT "Producto_pkey" PRIMARY KEY ("idProducto")
);

-- CreateTable
CREATE TABLE "Cliente" (
    "idCliente" TEXT NOT NULL,
    "Rif" TEXT NOT NULL,
    "Cliente" TEXT NOT NULL,
    "Zona" TEXT NOT NULL,
    "idAsesor" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "createdBy" TEXT NOT NULL,
    "updatedBy" TEXT NOT NULL,

    CONSTRAINT "Cliente_pkey" PRIMARY KEY ("idCliente")
);

-- CreateTable
CREATE TABLE "Pedido" (
    "idPedido" TEXT NOT NULL,
    "idEmpresa" INTEGER NOT NULL,
    "fechaPedido" TIMESTAMP(3) NOT NULL,
    "totalPedido" DOUBLE PRECISION NOT NULL,
    "idAsesor" TEXT NOT NULL,
    "Status" TEXT NOT NULL,
    "idCliente" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "createdBy" TEXT NOT NULL,
    "updatedBy" TEXT NOT NULL,

    CONSTRAINT "Pedido_pkey" PRIMARY KEY ("idPedido")
);

-- CreateTable
CREATE TABLE "DetallePedido" (
    "id" TEXT NOT NULL,
    "idPedido" TEXT NOT NULL,
    "idProducto" TEXT NOT NULL,
    "Precio" DOUBLE PRECISION NOT NULL,
    "Cantidad" INTEGER NOT NULL,
    "Total" DOUBLE PRECISION NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "createdBy" TEXT NOT NULL,
    "updatedBy" TEXT NOT NULL,

    CONSTRAINT "DetallePedido_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Empresa" (
    "idEmpresa" SERIAL NOT NULL,
    "RazonSocial" TEXT NOT NULL,
    "idPedido" INTEGER NOT NULL,
    "idRecibo" INTEGER NOT NULL,

    CONSTRAINT "Empresa_pkey" PRIMARY KEY ("idEmpresa")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_username_key" ON "User"("username");

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Asesor_idAsesor_key" ON "Asesor"("idAsesor");

-- CreateIndex
CREATE UNIQUE INDEX "Producto_idProducto_key" ON "Producto"("idProducto");

-- CreateIndex
CREATE UNIQUE INDEX "Cliente_Rif_key" ON "Cliente"("Rif");

-- CreateIndex
CREATE UNIQUE INDEX "Pedido_idPedido_key" ON "Pedido"("idPedido");

-- AddForeignKey
ALTER TABLE "Cliente" ADD CONSTRAINT "Cliente_idAsesor_fkey" FOREIGN KEY ("idAsesor") REFERENCES "Asesor"("idAsesor") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Pedido" ADD CONSTRAINT "Pedido_idAsesor_fkey" FOREIGN KEY ("idAsesor") REFERENCES "Asesor"("idAsesor") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Pedido" ADD CONSTRAINT "Pedido_idCliente_fkey" FOREIGN KEY ("idCliente") REFERENCES "Cliente"("idCliente") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "DetallePedido" ADD CONSTRAINT "DetallePedido_idPedido_fkey" FOREIGN KEY ("idPedido") REFERENCES "Pedido"("idPedido") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "DetallePedido" ADD CONSTRAINT "DetallePedido_idProducto_fkey" FOREIGN KEY ("idProducto") REFERENCES "Producto"("idProducto") ON DELETE RESTRICT ON UPDATE CASCADE;
