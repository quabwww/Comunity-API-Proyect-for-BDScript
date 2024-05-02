import importlib.util
import os


def registrar_rutas_desde_directorio(router, directorio):
    for nombre_archivo in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, nombre_archivo)
        if os.path.isdir(ruta_completa):
            registrar_rutas_desde_directorio(router, ruta_completa)
        elif nombre_archivo.endswith('.py') and nombre_archivo != '__init__.py':
            nombre_modulo = nombre_archivo[:-3]
            spec = importlib.util.spec_from_file_location(f"API.{nombre_modulo}", ruta_completa)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            if hasattr(modulo, 'router'):
                router.include_router(modulo.router)