ALTER TABLE suscripcion ADD CONSTRAINT suscripcion_id_region_foreign FOREIGN KEY (id_region) REFERENCES psn_region(id_psn);

ALTER TABLE lang_disp_int ADD CONSTRAINT lang_disp_int_id_juego_foreign FOREIGN KEY (id_juego) REFERENCES info_juego(id_juego);
ALTER TABLE lang_disp_int ADD CONSTRAINT lang_disp_int_id_lang_foreign FOREIGN KEY (id_lang) REFERENCES lang_disp(id_lang);

ALTER TABLE precio ADD CONSTRAINT precio_id_suscripcion_foreign FOREIGN KEY (id_suscripcion) REFERENCES suscripcion(id_suscripcion);
ALTER TABLE precio ADD CONSTRAINT precio_id_juego_foreign FOREIGN KEY (id_juego) REFERENCES info_juego(id_juego);

ALTER TABLE plat_int ADD CONSTRAINT plat_int_id_juego_foreign FOREIGN KEY (id_juego) REFERENCES info_juego(id_juego);
ALTER TABLE plat_int ADD CONSTRAINT plat_int_id_plat_foreign FOREIGN KEY (id_plat) REFERENCES plataforma(id_plataforma);

ALTER TABLE genero_int ADD CONSTRAINT genero_int_id_genero_foreign FOREIGN KEY (id_genero) REFERENCES genero(id_genero);
ALTER TABLE genero_int ADD CONSTRAINT genero_int_id_juego_foreign FOREIGN KEY (id_juego) REFERENCES info_juego(id_juego);

ALTER TABLE compania_int ADD CONSTRAINT compania_int_id_compania_foreign FOREIGN KEY (id_compania) REFERENCES compania(id_compania);
ALTER TABLE compania_int ADD CONSTRAINT compania_int_id_juego_foreign FOREIGN KEY (id_juego) REFERENCES info_juego(id_juego);
