#import tkinter as tk
#from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd

# Contexto inicial con pandas
contexto = {"pd": pd}

# Función por defecto para clasificar exclusiones (editable en la interfaz)

def clasificar_exclusiones(row):
    exclusiones = []

    if row.get("PQR Activa") == "Activa":
        exclusiones.append("PQR")

    if not exclusiones and row.get("Tutela") == "S":
        exclusiones.append("Tutela")

    nombre_subcuenta = str(row.get("Nombre Subcuenta", "")).lower()
    if not exclusiones and "fundaciones" in nombre_subcuenta:
        exclusiones.append("Capital")

    if not exclusiones and row.get("Rango Prioridad") == "Rojo":
        exclusiones.append("Ponderación Prioridad")

    if not exclusiones and row.get("Map") == "MAP":
        exclusiones.append("MAP")

    if not exclusiones and row.get("Nombre Cliente") == "ECOPETROL S.A (BOGOTA)":
        exclusiones.append("Acuerdo Ecopetrol")

    if not exclusiones and row.get("Nombre Cliente") == "ENTIDAD PROMOTORA DE SALUD SANITAS S A S - EN INTERVENCION BAJO LA MEDIDA DE TOMA DE POSESION (BOGOTA)":
        exclusiones.append("Acuerdo Sanitas")

    if not exclusiones:
        nombre_caf = str(row.get("Nombre Caf", "")).lower()
        dias_pendientes = row.get("Dias Pendientes Habiles")
        try:
            if "ips" in nombre_caf and pd.notna(dias_pendientes):
                dias_pendientes = float(dias_pendientes)
                if dias_pendientes <= 29:
                    exclusiones.append("Unidad Negocio IPS")
        except (ValueError, TypeError):
            pass

    if not exclusiones:
        nivel_iii = str(row.get("Nivel III", "")).lower()
        municipio = str(row.get("Municipio", "")).strip().lower()
        municipios_excluir = {"bogota", "soacha", "funza", "facatativa", "chia", "zipaquira"}

        if "pañales" in nivel_iii and municipio in municipios_excluir:
            exclusiones.append("Exclusion Pañales")

    valor_encomienda = row.get("S Id Encomienda")
    if not exclusiones and pd.notna(valor_encomienda) and str(valor_encomienda).strip() != "":
        exclusiones.append("Domi S gestionado")

    if not exclusiones and row.get("Tipo Domicilio Inicial") == "Central Pendientes":
        exclusiones.append("Central Pendientes")

    if not exclusiones and pd.notna(row.get("Fecha Cancelar")):
        try:
            fecha_cancelar = pd.to_datetime(row.get("Fecha Cancelar"))
            fecha_actual = pd.Timestamp.now()
            if fecha_cancelar > fecha_actual:
                exclusiones.append("Usuario Contactado")
        except ValueError:
            pass

    if not exclusiones:
        dias_pendientes = row.get("Dias Pendientes Habiles")
        valor_copago = row.get("G Copago")

        if pd.notna(dias_pendientes) and float(dias_pendientes) <= 29:
            if (
                pd.notna(valor_copago)
                and str(valor_copago).strip() != ""
                and float(valor_copago) != 0
            ):
                exclusiones.append("Valor Copago")
                
    return ", ".join(exclusiones)
