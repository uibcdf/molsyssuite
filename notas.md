Lee primero devguide/README.md y después todo el directorio devguide/.
No cambies las decisiones, menús, colecciones ni tags sin proponerlo explícitamente.
Objetivo: crear el scaffold mínimo ejecutable del sitio Astro dentro de web/ con rutas del MVP, content collections y un layout minimalista “less is more”.
Después: añade un workflow de GitHub Actions para publicar a gh-pages (sin tocar el contenido de devguide/).
Haz commits pequeños y describe lo que cambias.

Orden de trabajo (para evitar atascarte)
Scaffold Astro en web/ que corra y buildée.
Content Collections (schemas + lectura de Markdown)
Rutas MVP (páginas vacías pero conectadas a contenido)
Home con “latest 3–5”
Deploy gh-pages con Actions

Detalle importante según repo
Lab (root): base /
MolSysSuite (subpath): base /molsyssuite/ (no lo olvides, o se romperán assets)
Startup: base / (dominio TBD)
