# db_config

"""
Implementa un patrón de diseño DTO (Data Transfer Object). 
Este diseño se utiliza para transportar datos entre distintas
partes de un sistema
Básicamente, este archivo contiene solo datos y no lógica.

https://www.oscarblancarteblog.com/2018/11/30/data-transfer-object-dto-patron-diseno/
https://dev.to/izabelakowal/some-ideas-on-how-to-implement-dtos-in-python-be3
"""

from __future__ import annotations
from dataclasses import dataclass
import os

"""
Clase DBConfig:
Agrupa todos los parámetros en un solo objeto
"""

@dataclass(frozen=True)
class DBConfig:
    """
    Contiene la configuración de conexión a Oracle vía ODBC.
    """
    driver: str             #Nombre EXACTO del driver ODBC (tal como sale en pyodbc.drivers())
    host: str               #"oracle0.ugr.es"
    port: int               #1521
    service_name: str       #"practbd"
    user: str               #"xloquesea"
    password: str           #"xloquesea"
    autocommit: bool = False    #Autocommit se refiere a si cada vez que se envía sentencia SQL se ejecuta al momento, no interesa
    pooling: bool = True        #Pooling mantiene un grupo de conexiones, renta a true

    """
    Junta los atributos en una cadena con el formato oracle
    Ej. Cadena:
    DRIVER={Oracle in instantclient_21_13};DBQ=//oracle0.ugr.es:1521/practbd;UID=usuario;PWD=contraseña;Pooling=Yes
    
    Es una propiedad de la clase, se usará como: config.odbc_conn_str
    """
    @property
    def odbc_convertir(self) -> str:
        parts = [
            f"DRIVER={{{self.driver}}}",
            f"DBQ=//{self.host}:{self.port}/{self.service_name}",
            f"UID={self.user}",
            f"PWD={self.password}",
        ]
        if self.pooling:
            parts.append("Pooling=Yes")
        return ";".join(parts)

"""
Carga la configuración de las variables de entorno
IMPORTANTE: Cada uno tendrá que tener sus variables de entorno previamente configuradas

$ python -c "import pyodbc; print(pyodbc.drivers())" #Comprobar driver
#Asignar variables de entorno
$ export ORACLE_DRIVER="Oracle in instantclient_23_26"
$ export ORACLE_HOST="oracle0.ugr.es"
$ export ORACLE_PORT="1521"
$ export ORACLE_SERVICE="practbd"
$ export ORACLE_USER="x########"
$ export ORACLE_PASSWORD="x########"

Devuelve un objeto de la clase DBConfig con la información
"""
def from_env() -> DBConfig:
    required = [
        "ORACLE_DRIVER", "ORACLE_HOST", "ORACLE_PORT",
        "ORACLE_SERVICE", "ORACLE_USER", "ORACLE_PASSWORD"
    ]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise RuntimeError(
            "Faltan variables de entorno: " + ", ".join(missing) +
            ". Define ORACLE_DRIVER, ORACLE_HOST, ORACLE_PORT, "
            "ORACLE_SERVICE, ORACLE_USER, ORACLE_PASSWORD."
        )

    return DBConfig(
        driver=os.environ["ORACLE_DRIVER"],       
        host=os.environ["ORACLE_HOST"],           
        port=int(os.environ["ORACLE_PORT"]),      
        service_name=os.environ["ORACLE_SERVICE"],
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        autocommit=False,
        pooling=True,
    )
