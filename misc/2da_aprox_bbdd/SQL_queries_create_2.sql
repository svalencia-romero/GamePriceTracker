CREATE TABLE "suscripcion"(
    "id_suscripcion" SERIAL PRIMARY KEY ,
    "nombre_suscripcion" VARCHAR(30) NOT NULL,
    "id_region" BIGINT NOT NULL
);

CREATE TABLE "lang_disp"(
    "id_lang" SERIAL PRIMARY KEY,
    "nombre_lang" BIGINT NOT NULL
);

CREATE TABLE "precio"(
    "id_precio" SERIAL PRIMARY KEY,
    "id_suscripcion" BIGINT NOT NULL,
    "precio" BIGINT NOT NULL,
    "id_fecha" BIGINT NOT NULL,
    "id_juego" BIGINT NOT NULL
);

CREATE TABLE "fecha"(
    "id_fecha" SERIAL PRIMARY KEY,
    "fecha_scrap" DATE NOT NULL
);

CREATE TABLE "genero"(
    "id_genero" SERIAL PRIMARY KEY,
    "genero" VARCHAR(30) NOT NULL
);

CREATE TABLE "info_juego"(
    "id_juego" BIGINT PRIMARY KEY,
    "nombre" VARCHAR(50) NOT NULL,
    "id_compania" BIGINT NOT NULL,
    "numero calificaciones" BIGINT NOT NULL,
    "num_calficaciones_5_estrellas" BIGINT NOT NULL,
    "num_calficaciones_4_estrellas" BIGINT NOT NULL,
    "num_calficaciones_3_estrellas" BIGINT NOT NULL,
    "num_calficaciones_2_estrellas" BIGINT NOT NULL,
    "num_calficaciones_1_estrellas" BIGINT NOT NULL,
    "id_camp" BIGINT NOT NULL,
    "id_platafrm" BIGINT NOT NULL,
    "calificacion_psn" BIGINT NOT NULL
);

CREATE TABLE "plat_int"(
    "id_interm" SERIAL PRIMARY KEY,
    "id_plat" BIGINT NOT NULL,
    "id_juego" BIGINT NOT NULL
);

CREATE TABLE "genero_int"(
    "id_gen_int" SERIAL PRIMARY KEY, 
    "id_genero" BIGINT NOT NULL,
    "id_juego" BIGINT NOT NULL
);

CREATE TABLE "lang_disp_int"(
    "id_lang_int" SERIAL PRIMARY KEY,
    "id_juego" BIGINT NOT NULL,
    "id_lang" BIGINT NOT NULL
);

CREATE TABLE "compañia"(
    "id_compania" SERIAL PRIMARY KEY,
    "nombre_compañia" VARCHAR(30) NOT NULL
);

CREATE TABLE "plataforma"(
    "id_plataforma" SERIAL PRIMARY KEY,
    "nombre_plataforma" VARCHAR(20) NOT NULL
);

CREATE TABLE "psn_region"(
    "id_psn" SERIAL PRIMARY KEY,
    "region" VARCHAR(20) NOT NULL
);

ALTER TABLE
    "suscripcion" ADD CONSTRAINT "suscripcion_id_region_foreign" FOREIGN KEY("id_region") REFERENCES "psn_region"("id_psn");
ALTER TABLE
    "precio" ADD CONSTRAINT "precio_id_fecha_foreign" FOREIGN KEY("id_fecha") REFERENCES "fecha"("id_fecha");
ALTER TABLE
    "lang_disp_int" ADD CONSTRAINT "lang_disp_int_id_juego_foreign" FOREIGN KEY("id_juego") REFERENCES "info_juego"("id_juego");
ALTER TABLE
    "lang_disp_int" ADD CONSTRAINT "lang_disp_int_id_lang_foreign" FOREIGN KEY("id_lang") REFERENCES "lang_disp"("id_lang");
ALTER TABLE
    "precio" ADD CONSTRAINT "precio_id_suscripcion_foreign" FOREIGN KEY("id_suscripcion") REFERENCES "suscripcion"("id_suscripcion");
ALTER TABLE
    "plat_int" ADD CONSTRAINT "plat_int_id_juego_foreign" FOREIGN KEY("id_juego") REFERENCES "info_juego"("id_juego");
ALTER TABLE
    "genero_int" ADD CONSTRAINT "genero_int_id_genero_foreign" FOREIGN KEY("id_genero") REFERENCES "genero"("id_genero");
ALTER TABLE
    "precio" ADD CONSTRAINT "precio_id_juego_foreign" FOREIGN KEY("id_juego") REFERENCES "info_juego"("id_juego");
ALTER TABLE
    "plat_int" ADD CONSTRAINT "plat_int_id_plat_foreign" FOREIGN KEY("id_plat") REFERENCES "plataforma"("id_plataforma");
ALTER TABLE
    "info_juego" ADD CONSTRAINT "info_juego_id_compania_foreign" FOREIGN KEY("id_compania") REFERENCES "compañia"("id_compania");
ALTER TABLE
    "genero_int" ADD CONSTRAINT "genero_int_id_juego_foreign" FOREIGN KEY("id_juego") REFERENCES "info_juego"("id_juego");