FROM postgres:latest

# Set environment variables
ENV POSTGRES_USER=InvestorPro
ENV POSTGRES_PASSWORD=123456!@
ENV POSTGRES_DB=AppDataBase

# Create and set permissions for the data directory
RUN mkdir -p /var/lib/postgresql/data
RUN chown -R postgres:postgres /var/lib/postgresql/data

# Optionally, set maximum memory capacity for PostgreSQL
# Note: This depends on the available system resources
ENV PG_MAX_CONNECTIONS=100
ENV PG_SHARED_BUFFERS=2GB

# Copy SQL initialization scripts
#COPY init.sql /docker-entrypoint-initdb.d/