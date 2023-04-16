FROM postgres:12-alpine

RUN rm /var/lib/postgresql/data/pg_hba.conf
COPY pg_hba.conf /var/lib/postgresql/data/pg_hba.conf