# NexoPay API demo

API de prueba para el proyecto integrador de Infraestructura en la Nube (UNIMINUTO).

- Ejecutar localmente: `pip install -r requirements.txt` y `uvicorn main:app --reload`
- Pruebas: `pytest -q`
- Comando de inicio en Azure App Service:
  `gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app`
- Prueba de carga: `python carga.py https://TU-APP.azurewebsites.net 600`
