CREATE TABLE "precio_campana"(
    "id_camp" BIGINT NOT NULL,
    "nombre_camp" VARCHAR(255) NOT NULL,
    "precio_camp" BIGINT NOT NULL,
    "id_region" BIGINT NOT NULL,
    "time_scrap" DATE NOT NULL
);
ALTER TABLE
    "precio_campana" ADD PRIMARY KEY("id_camp");
CREATE TABLE "lang_disp"(
    "id_lang" BIGINT NOT NULL,
    "nombre_lang" BIGINT NOT NULL
);
ALTER TABLE
    "lang_disp" ADD PRIMARY KEY("id_lang");
CREATE TABLE "genero"(
    "id_genero" BIGINT NOT NULL,
    "genero" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "genero" ADD PRIMARY KEY("id_genero");
CREATE TABLE "info_juego"(
    "id_juego" BIGINT NOT NULL,
    "nombre" VARCHAR(255) NOT NULL,
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
ALTER TABLE
    "info_juego" ADD PRIMARY KEY("id_juego");
CREATE TABLE "camp_interm"(
    "id_camp_intermedia" BIGINT NOT NULL,
    "id_precio_camp" BIGINT NOT NULL,
    "id_juego" BIGINT NOT NULL
);
ALTER TABLE
    "camp_interm" ADD PRIMARY KEY("id_camp_intermedia");
CREATE TABLE "plat_int"(
    "id_interm" BIGINT NOT NULL,
    "id_plat" BIGINT NOT NULL,
    "id_juego" BIGINT NOT NULL
);
ALTER TABLE
    "plat_int" ADD PRIMARY KEY("id_interm");
CREATE TABLE "genero_int"(
    "id_gen_int" BIGINT NOT NULL,
    "id_genero" BIGINT NOT NULL,
    "id_juego" BIGINT NOT NULL
);
ALTER TABLE
    "genero_int" ADD PRIMARY KEY("id_gen_int");
CREATE TABLE "lang_disp_int"(
    "id_lang_int" BIGINT NOT NULL,
    "id_juego" BIGINT NOT NULL,
    "id_lang" BIGINT NOT NULL
);
ALTER TABLE
    "lang_disp_int" ADD PRIMARY KEY("id_lang_int");
CREATE TABLE "compañia"(
    "id_compania" BIGINT NOT NULL,
    "nombre_compañia" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "compañia" ADD PRIMARY KEY("id_compania");
CREATE TABLE "plataforma"(
    "id_plataforma" BIGINT NOT NULL,
    "nombre_plataforma" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "plataforma" ADD PRIMARY KEY("id_plataforma");
CREATE TABLE "psn_region"(
    "id_psn" BIGINT NOT NULL,
    "region" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "psn_region" ADD PRIMARY KEY("id_psn");
ALTER TABLE
    "precio_campana" ADD CONSTRAINT "precio_campana_id_region_foreign" FOREIGN KEY("id_region") REFERENCES "psn_region"("id_psn");
ALTER TABLE
    "camp_interm" ADD CONSTRAINT "camp_interm_id_precio_camp_foreign" FOREIGN KEY("id_precio_camp") REFERENCES "precio_campana"("id_camp");
ALTER TABLE
    "lang_disp_int" ADD CONSTRAINT "lang_disp_int_id_juego_foreign" FOREIGN KEY("id_juego") REFERENCES "info_juego"("id_juego");
ALTER TABLE
    "lang_disp_int" ADD CONSTRAINT "lang_disp_int_id_lang_foreign" FOREIGN KEY("id_lang") REFERENCES "lang_disp"("id_lang");
ALTER TABLE
    "plat_int" ADD CONSTRAINT "plat_int_id_juego_foreign" FOREIGN KEY("id_juego") REFERENCES "info_juego"("id_juego");
ALTER TABLE
    "genero_int" ADD CONSTRAINT "genero_int_id_genero_foreign" FOREIGN KEY("id_genero") REFERENCES "genero"("id_genero");
ALTER TABLE
    "camp_interm" ADD CONSTRAINT "camp_interm_id_juego_foreign" FOREIGN KEY("id_juego") REFERENCES "info_juego"("id_juego");
ALTER TABLE
    "plat_int" ADD CONSTRAINT "plat_int_id_plat_foreign" FOREIGN KEY("id_plat") REFERENCES "plataforma"("id_plataforma");
ALTER TABLE
    "info_juego" ADD CONSTRAINT "info_juego_id_compania_foreign" FOREIGN KEY("id_compania") REFERENCES "compañia"("id_compania");
ALTER TABLE
    "genero_int" ADD CONSTRAINT "genero_int_id_juego_foreign" FOREIGN KEY("id_juego") REFERENCES "info_juego"("id_juego");