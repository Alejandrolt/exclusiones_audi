"""Módulo para clasificar exclusiones en domicilios médicos."""

import pandas as pd

def clasificar_exclusiones(row):
    """Clasifica una fila de datos según criterios de exclusión médica."""
    exclusiones = []

    if row.get("PQR Activa") == "Activa":
        exclusiones.append("PQR")

    if not exclusiones and row.get("Tutela") == "S":
        exclusiones.append("Tutela")

    nombre_subcuenta = str(row.get("Nombre Subcuenta", "")).lower()
    if not exclusiones and "fundaciones" in nombre_subcuenta:
        exclusiones.append("Capital")

    if not exclusiones and row.get("Map") == "MAP":
        exclusiones.append("MAP")

    if not exclusiones and row.get("Nombre Cliente") == "ECOPETROL S.A (BOGOTA)":
        exclusiones.append("Acuerdo Ecopetrol")

    if not exclusiones and row.get("Nombre Cliente") == (
    "ENTIDAD PROMOTORA DE SALUD SANITAS S A S - EN INTERVENCION BAJO "
    "LA MEDIDA DE TOMA DE POSESION (BOGOTA)"
):
        exclusiones.append("Acuerdo Sanitas")

    if not exclusiones and row.get("Rango Prioridad") == "Rojo":
        exclusiones.append("Ponderación Prioridad")

    if not exclusiones:
        nombre_caf = str(row.get("Nombre Caf", "")).lower()
        dias_pendientes = row.get("Dias Pendientes Habiles")
        try:
            if "ips" in nombre_caf and pd.notna(dias_pendientes):
                dias_pendientes = float(dias_pendientes)
                if dias_pendientes <= 24:
                    exclusiones.append("Unidad Negocio IPS")
        except (ValueError, TypeError):
            pass

    valor_encomienda = row.get("S Id Encomienda")
    if not exclusiones and pd.notna(valor_encomienda) and str(valor_encomienda).strip() != "":
        exclusiones.append("Domi S gestionado")

    if not exclusiones and row.get("Tipo Domicilio Inicial") == "Central Pendientes":
        exclusiones.append("Central Pendientes")

    if not exclusiones and pd.notna(row.get("Fecha Cancelar")):
        try:
            fecha_cancelar = pd.to_datetime(row.get("Fecha Cancelar"))
            if fecha_cancelar > pd.Timestamp.now():
                exclusiones.append("Usuario Contactado")
        except (ValueError, TypeError):
            pass

    return ", ".join(exclusiones)
