# TICKET 4 — Reporte de envíos (DistriPura)
# Todo en este archivo. El archivo envios.csv ya está en esta carpeta (tiene filas dañadas a propósito).
import csv
from pathlib import Path

# Tarifas del Ticket #2 (defínelas UNA sola vez)
BASE = {"A": 2500, "B": 3500, "C": 5000}
KG_INCLUIDOS = 5
COSTO_KG_EXTRA = 400
PESO_MAXIMO = 50


class Envio:

    def __init__(self, id, cliente, peso_kg, zona):
        self.id = id
        self.cliente = cliente
        self.peso_kg = peso_kg
        self.zona = zona

    def costo(self):

        tarifa_base = BASE[self.zona]

        peso_extra = max(0, self.peso_kg - KG_INCLUIDOS)

        costo_extra = peso_extra * COSTO_KG_EXTRA

        return tarifa_base + costo_extra
         

def cargar_envios(ruta):

    validos = []
    errores = []

    with open(ruta, "r", encoding="utf-8", newline="") as archivo:

        lector = csv.DictReader(archivo)

        for numero_fila, fila in enumerate(lector, start=2):

            try:
                # 1. Validar que existan las 4 columnas
                columnas = ["id", "cliente", "peso_kg", "zona"]

                if None in fila or any(fila.get(c) is None for c in columnas):
                    raise ValueError("faltan columnas")
                
                 # 2. Validar que el cliente no esté vacío
                cliente = fila["cliente"].strip()

                if not cliente:
                    raise ValueError("cliente vacío")

                try:
                    # 3. Convertir el peso a entero
                    peso = int(fila["peso_kg"])
                except ValueError:
                    raise ValueError("peso no numérico")
                
                # 4. Validar que el peso sea mayor que 0
                if peso <= 0:
                    raise ValueError("peso negativo")
                
                # 5. Validar que el peso no supere los 50 kg
                if peso > PESO_MAXIMO:
                    raise ValueError("peso supera los 50 kg")
                
                # 6. Validar la zona
                zona = fila["zona"].strip().upper()

                if zona not in BASE:
                    raise ValueError("zona inválida")
                
                # 7. Crear el objeto solamente si pasó todas las validaciones
                pedido = Envio(
                    fila["id"],
                    cliente,
                    peso,
                    zona
                )

                validos.append(pedido)

            except (ValueError, KeyError) as error:

                errores.append({
                    "linea": numero_fila,
                    "motivo": str(error)
                })

    total_cobrado = sum(envio.costo() for envio in validos)

    print("\n========== REPORTE DE ENVÍOS ==========")
    print(f"Cantidad de envíos válidos: {len(validos)}")
    print(f"Total cobrado: ₡{total_cobrado:,.0f}")

    print("\nLíneas rechazadas:")

    if errores:
        for error in errores:
            print(f"Línea {error['linea']}: {error['motivo']}")
    else:
        print("No se rechazaron envíos.")

    print("=======================================\n")

    return validos, errores



if __name__ == "__main__":
    ruta_csv = Path(__file__).parent / "envios.csv"
    validos, errores = cargar_envios(ruta_csv)