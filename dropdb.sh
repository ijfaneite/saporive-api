# Matar conexiones y borrar la base de datos
PGPASSWORD='e7VjxmKfjMYbYjXNAIhP4TnyWM7czBGy@dpg-d5iqv12li9vc73ahpc9g-a.virginia-saporidb_user.render.com' sudo psql -U saporidb_user -d saporidb -c "DROP DATABASE \"saporiDB\";"


PGPASSWORD='e7VjxmKfjMYbYjXNAIhP4TnyWM7czBGy@dpg-d5iqv12li9vc73ahpc9g-a.virginia-saporidb_user.render.com'  sudo psql -U saporidb_user -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'saporidb';"
PGPASSWORD='e7VjxmKfjMYbYjXNAIhP4TnyWM7czBGy@dpg-d5iqv12li9vc73ahpc9g-a.virginia-saporidb_user.render.com'  sudo psql -U saporidb_user -c "DROP DATABASE \"saporidb\";"

# Crear la base de datos limpia
PGPASSWORD='e7VjxmKfjMYbYjXNAIhP4TnyWM7czBGy@dpg-d5iqv12li9vc73ahpc9g-a.virginia-saporidb_user.render.com' sudo psql -U saporidb_user -c "CREATE DATABASE \"saporidb\";"

# Volver a empujar el esquema de Prisma
python -m prisma db push
python -m prisma generate