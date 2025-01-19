# Project Setup

## Environment Variables

1. Set the following environment variable in a `env` file:

```env
# Please set your OPENAI_API_KEY here:
OPENAI_API_KEY=your_openai_api_key_here
```

2. Rename `env` to `.env`.

## Commands

### Be sure to have MongoDB set up:

```bash
bash setup/setup_mongodb_<Your-OS-goes-here>.sh
```

### To Start the Project

Run the following command to start the project:

```bash
docker compose --env-file .env up -d
```

### To Stop the Project

Run the following command to stop the project:

```bash
docker compose --env-file .env down
```

### To Build Without Cache

If you need to build without using the cache, you can use the following commands:

```bash
docker compose build --no-cache
docker compose --env-file .env up -d
```

