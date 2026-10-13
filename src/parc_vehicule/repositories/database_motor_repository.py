from parc_vehicule.models.motorisations.electrique import Electrique
from parc_vehicule.models.motorisations.hybride import Hybride
from parc_vehicule.models.motorisations.thermique import Thermique
from parc_vehicule.repositories.abstractmotorrepository import AbstractMotorRepository


class DatabaseMotorRepository(AbstractMotorRepository):

    def __init__(self, connection):
        self._conn = connection

    def _from_row(self, row):
        if row is None:
            return None
        motor_id, typ, power, conso_th, cap_th, conso_el, cap_el = row
        t = typ.lower()
        kwargs = {} if (power is None or power == 0) else {"power": power}
        if t in ("thermique", "thermic"):
            m = Thermique(float(cap_th), float(conso_th), **kwargs)
        elif t in ("electrique", "electric", "électrique"):
            m = Electrique(float(cap_el), float(conso_el), **kwargs)
        elif t in ("hybride", "hybrid"):
            m = Hybride(float(cap_th), float(conso_th), float(cap_el), float(conso_el), **kwargs)
        else:
            raise ValueError(f"Type de motorisation inconnu : {typ!r}")
        m.id = motor_id
        return m

    def add(self, motor) -> int:
        cursor = self._conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO motors (type, power, consumption_thermic, capacity_thermic,
                   consumption_electric, capacity_electric)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    getattr(motor, "type", None),
                    getattr(motor, "power", None) or 0,
                    getattr(motor, "consumption_thermic", None),
                    getattr(motor, "capacity_thermic", None),
                    getattr(motor, "consumption_electric", None),
                    getattr(motor, "capacity_electric", None),
                ),
            )
            self._conn.commit()
            motor.id = cursor.lastrowid
            return motor.id
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cursor.close()

    def get_by_id(self, motor_id: int):
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM motors WHERE id = %s", (motor_id,))
            return self._from_row(cursor.fetchone())
        finally:
            cursor.close()

    def read_all(self) -> list:
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM motors")
            return [self._from_row(r) for r in cursor.fetchall()]
        finally:
            cursor.close()

    def update(self, motor) -> bool:
        cursor = self._conn.cursor()
        try:
            cursor.execute(
                """UPDATE motors SET type=%s, power=%s, consumption_thermic=%s,
                   capacity_thermic=%s, consumption_electric=%s, capacity_electric=%s
                   WHERE id=%s""",
                (
                    motor.type,
                    getattr(motor, "power", None),
                    getattr(motor, "consumption_thermic", None),
                    getattr(motor, "capacity_thermic", None),
                    getattr(motor, "consumption_electric", None),
                    getattr(motor, "capacity_electric", None),
                    motor.id,
                ),
            )
            self._conn.commit()
            return cursor.rowcount > 0
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cursor.close()

    def delete(self, motor_id: int) -> bool:
        cursor = self._conn.cursor()
        try:
            cursor.execute("DELETE FROM motors WHERE id = %s", (motor_id,))
            self._conn.commit()
            return cursor.rowcount > 0
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cursor.close()
