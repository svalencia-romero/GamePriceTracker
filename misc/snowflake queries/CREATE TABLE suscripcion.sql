CREATE TABLE suscripcion (
    id_suscripcion NUMBER PRIMARY KEY DEFAULT suscripcion_id_seq.NEXTVAL,
    nombre_suscripcion VARCHAR(30) NOT NULL,
    id_region BIGINT NOT NULL
);

CREATE TABLE lang_disp (
    id_lang NUMBER PRIMARY KEY DEFAULT lang_disp_id_seq.NEXTVAL,
    nombre_lang VARCHAR(50)
);

CREATE TABLE precio (
    id_precio NUMBER PRIMARY KEY DEFAULT precio_id_seq.NEXTVAL,
    id_suscripcion BIGINT NOT NULL,
    precio FLOAT NOT NULL,
    fecha_webs TIMESTAMP NOT NULL,
    id_juego BIGINT NOT NULL
);

CREATE TABLE genero (
    id_genero NUMBER PRIMARY KEY DEFAULT genero_id_seq.NEXTVAL,
    genero VARCHAR(30) NOT NULL
);

CREATE TABLE info_juego (
    id_juego BIGINT PRIMARY KEY,
    nombre VARCHAR(190) NOT NULL,
    numero_calificaciones BIGINT NOT NULL,
    num_calificaciones_5_estrellas BIGINT NOT NULL,
    num_calificaciones_4_estrellas BIGINT NOT NULL,
    num_calificaciones_3_estrellas BIGINT NOT NULL,
    num_calificaciones_2_estrellas BIGINT NOT NULL,
    num_calificaciones_1_estrellas BIGINT NOT NULL,
    calificacion_psn FLOAT NOT NULL,
    lanzamiento DATE NOT NULL
);

CREATE TABLE plat_int (
    id_interm NUMBER PRIMARY KEY DEFAULT plat_int_id_seq.NEXTVAL,
    id_plat BIGINT NOT NULL,
    id_juego BIGINT NOT NULL
);

CREATE TABLE genero_int (
    id_gen_int NUMBER PRIMARY KEY DEFAULT genero_int_id_seq.NEXTVAL,
    id_genero BIGINT NOT NULL,
    id_juego BIGINT NOT NULL
);

CREATE TABLE lang_disp_int (
    id_lang_int NUMBER PRIMARY KEY DEFAULT lang_disp_int_id_seq.NEXTVAL,
    id_juego BIGINT NOT NULL,
    id_lang BIGINT NOT NULL
);

CREATE TABLE compania (
    id_compania NUMBER PRIMARY KEY DEFAULT compania_id_seq.NEXTVAL,
    nombre_compania VARCHAR(70) NOT NULL
);

CREATE TABLE plataforma (
    id_plataforma NUMBER PRIMARY KEY DEFAULT plataforma_id_seq.NEXTVAL,
    nombre_plataforma VARCHAR(20) NOT NULL
);

CREATE TABLE psn_region (
    id_psn NUMBER PRIMARY KEY DEFAULT psn_region_id_seq.NEXTVAL,
    region VARCHAR(20) NOT NULL
);

CREATE TABLE compania_int (
    id_interm_compania NUMBER PRIMARY KEY DEFAULT compania_int_id_seq.NEXTVAL,
    id_compania BIGINT NOT NULL,
    id_juego BIGINT NOT NULL
);