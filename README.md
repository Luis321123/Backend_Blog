## Arquitectura del Sistema

<div align="center">
  <img src="image.png" alt="Diagrama de arquitectura">
</div>

<div align="center">

**Esta API de Blog sigue una arquitectura clara de 3 capas:**

</div>
<div align="center">

<br> 1. **Blog's UI (Interfaz de Usuario(en proceso))**:
     <br>
     <br> - Frontend que consume nuestra API RESTful
     <br> - Desarrollado con ReactJS
     <br> - Se comunica exclusivamente con la capa de la API

<br> 3. **Blog API (Capa de Servicio)**:
    <br>
   <br> - Desarrollada con FastAPI (Python)
     <br>  Proporciona endpoints RESTful para:
     <br> - Gestión de usuarios (registro, autenticación, perfiles)
     <br> - CRUD de artículos del blog
   <br>   - Comentarios y valoraciones
     <br> - Búsqueda y filtrado
   <br> - Valida datos y gestiona la lógica de negocio
  <br>  - Se comunica con la base de datos

<br> 4. **Database (Almacenamiento)**:
    <br>
    <br> - Base de datos PostgreSQL
    <br> - Almacena:
     <br> - Usuarios y credenciales
     <br> - Artículos del blog con su contenido
     <br>- Comentarios y relaciones
    <br> - Garantiza persistencia y consistencia de datos
</div>
<div align="center">

### Flujo típico:
<br>1. - El usuario realiza una acción en la UI  
<br>2. - La UI hace una petición HTTP a la API  
<br>3. - La API procesa la petición, interactúa con la DB si es necesario  
<br>4. - La API devuelve una respuesta JSON a la UI  
<br>5. - La UI actualiza su estado según la respuesta  

</div>
