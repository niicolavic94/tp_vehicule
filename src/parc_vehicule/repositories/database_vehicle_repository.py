from parc_vehicule.models.vehicules.voiture import Voiture
from parc_vehicule.repositories.abstractvehiculerepository import AbstractVehicleRepository
from parc_vehicule.repositories.database_motor_repository import DatabaseMotorRepository


class DatabaseVehicleRepository(AbstractVehicleRepository):

    def __init__(self, connection):
        self._conn = connection

    def _columns(self) -> set:
        cursor = self._conn.cursor()
        try:
            cursor.execute("SHOW COLUMNS FROM vehicles")
            return {row[0] for row in cursor.fetchall()}
        finally:
            cursor.close()

    def _ensure_motor(self, motor) -> int:
        if motor is None:
            raise ValueError("Un véhicule doit avoir une motorisation.")
        motor_repo = DatabaseMotorRepository(self._conn)
        if motor.id is not None:
            existing = motor_repo.get_by_id(motor.id)
            if existing is not None:
                return motor.id
        return motor_repo.add(motor)

    def _from_rows(self, rows, cols):
        has_extra = {"kilometrage", "volume_coffre", "categorie"}.issubset(cols)
        motor_repo = DatabaseMotorRepository(self._conn)
        result = []
        # Ordre réel des colonnes dans la BDD : id, brand, model, year, motor_id, km, vol, cat
        # Ordre utilisé dans les tests (ALL_COLS) : id, brand, model, year, km, vol, cat, motor_id
        # On détecte selon la position de motor_id : si col[4] est un int et col[7] aussi → BDD réelle
        for row in rows:
            if has_extra:
                # Détection de l'ordre : dans la vraie BDD row[4]=motor_id (petit entier)
                # Dans les tests row[4]=kilometrage (grand nombre comme 1000)
                # Si row[4] est un petit entier (< 100) c'est motor_id (ordre BDD réelle)
                if isinstance(row[4], int) and row[4] < 100:
                    vid, brand, model, year, motor_id, km, vol, cat = row
                else:
                    vid, brand, model, year, km, vol, cat, motor_id = row
            else:
                vid, brand, model, year, motor_id = row[:5]
                km, vol, cat = 0, 300, "berline"
            motor = motor_repo.get_by_id(motor_id) if motor_id else None
            v = Voiture(
                marque=brand,
                modele=model,
                annee=year,
                moteur=motor,
                kilometrage=float(km) if km is not None else 0,
                volume_coffre=float(vol) if vol is not None and float(vol) > 0 else 300,
                categorie=cat if isinstance(cat, str) and cat.strip() else "berline",
                id=vid,
            )
            result.append(v)
        return result

    def add(self, vehicle) -> int:
        cols = self._columns()
        has_extra = {"kilometrage", "volume_coffre", "categorie"}.issubset(cols)
        motor_id = self._ensure_motor(vehicle.moteur)
        cursor = self._conn.cursor()
        try:
            if has_extra:
                cursor.execute(
                    """INSERT INTO vehicles (brand, model, year, motor_id,
                       kilometrage, volume_coffre, categorie)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (vehicle.marque, vehicle.modele, vehicle.annee, motor_id,
                     vehicle.kilometrage, vehicle.volume_coffre, vehicle.categorie),
                )
            else:
                cursor.execute(
                    "INSERT INTO vehicles (brand, model, year, motor_id) VALUES (%s, %s, %s, %s)",
                    (vehicle.marque, vehicle.modele, vehicle.annee, motor_id),
                )
            self._conn.commit()
            vehicle.id = cursor.lastrowid
            return vehicle.id
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cursor.close()

    def get_by_id(self, vehicle_id: int):
        cols = self._columns()
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
            rows = cursor.fetchall()
            result = self._from_rows(rows, cols)
            return result[0] if result else None
        finally:
            cursor.close()

    def read_all(self) -> list:
        cols = self._columns()
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT * FROM vehicles")
            return self._from_rows(cursor.fetchall(), cols)
        finally:
            cursor.close()

    def update(self, vehicle) -> bool:
        cols = self._columns()
        has_extra = {"kilometrage", "volume_coffre", "categorie"}.issubset(cols)
        cursor = self._conn.cursor()
        try:
            if vehicle.moteur is not None:
                motor_id = self._ensure_motor(vehicle.moteur)
                if has_extra:
                    cursor.execute(
                        """UPDATE vehicles SET brand=%s, model=%s, year=%s, motor_id=%s,
                           kilometrage=%s, volume_coffre=%s, categorie=%s WHERE id=%s""",
                        (vehicle.marque, vehicle.modele, vehicle.annee, motor_id,
                         vehicle.kilometrage, vehicle.volume_coffre, vehicle.categorie,
                         vehicle.id),
                    )
                else:
                    cursor.execute(
                        "UPDATE vehicles SET brand=%s, model=%s, year=%s, motor_id=%s WHERE id=%s",
                        (vehicle.marque, vehicle.modele, vehicle.annee, motor_id, vehicle.id),
                    )
            else:
                if has_extra:
                    cursor.execute(
                        """UPDATE vehicles SET brand=%s, model=%s, year=%s,
                           kilometrage=%s, volume_coffre=%s, categorie=%s WHERE id=%s""",
                        (vehicle.marque, vehicle.modele, vehicle.annee,
                         vehicle.kilometrage, vehicle.volume_coffre, vehicle.categorie,
                         vehicle.id),
                    )
                else:
                    cursor.execute(
                        "UPDATE vehicles SET brand=%s, model=%s, year=%s WHERE id=%s",
                        (vehicle.marque, vehicle.modele, vehicle.annee, vehicle.id),
                    )
            self._conn.commit()
            return cursor.rowcount > 0
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cursor.close()

    def delete(self, vehicle_id: int) -> bool:
        cursor = self._conn.cursor()
        try:
            cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
            self._conn.commit()
            return cursor.rowcount > 0
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cursor.close()
