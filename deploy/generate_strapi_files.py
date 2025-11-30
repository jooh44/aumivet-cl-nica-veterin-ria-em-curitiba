import os

base_dir = "strapi-app"
dirs = [
    "api",
    "config",
    "config/functions",
    "extensions",
    "public",
    "public/uploads"
]

files = {
    "config/server.js": """module.exports = ({ env }) => ({
  host: env('HOST', '0.0.0.0'),
  port: env.int('PORT', 1337),
  admin: {
    auth: {
      secret: env('ADMIN_JWT_SECRET'),
    },
  },
});""",

    "config/database.js": """module.exports = ({ env }) => ({
  defaultConnection: 'default',
  connections: {
    default: {
      connector: 'bookshelf',
      settings: {
        client: env('DATABASE_CLIENT', 'postgres'),
        host: env('DATABASE_HOST', '127.0.0.1'),
        port: env.int('DATABASE_PORT', 5432),
        database: env('DATABASE_NAME', 'strapi'),
        username: env('DATABASE_USERNAME', 'strapi'),
        password: env('DATABASE_PASSWORD', 'strapi'),
      },
      options: {
        ssl: env.bool('DATABASE_SSL', false),
      },
    },
  },
});""",

    "public/index.html": """<!DOCTYPE html>
<html>
<head>
  <title>Aumivet Strapi</title>
</head>
<body>
  <h1>Strapi is running!</h1>
</body>
</html>""",

    "public/robots.txt": "User-agent: *\nDisallow: /"
}

# Create directories
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)
    print(f"Created directory: {d}")

# Create files
for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"Created file: {path}")
