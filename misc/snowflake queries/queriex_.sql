SELECT nombre AS Nombre_del_Juego,ROUND(AVG(PRECIO),2) as avg_precio, ROUND(MIN(PRECIO),2) as min_precio, ROUND(MAX(PRECIO),2) as max_precio
FROM precio
INNER JOIN info_juego ON info_juego.id_juego = precio.id_juego
WHERE id_suscripcion = 4 /*1 EU, 2 USA, 3 JAP normal ,4 EU, 5 USA, 6 JAP rebajado,7 EU, 8 USA, 9 JAP PSN,10 EU,11 USA, 12 JAP Otra suscripcion*/ AND LOWER(nombre) LIKE '%red dead%'
GROUP BY precio.id_juego, nombre
ORDER BY MAX(calificacion_psn) DESC,MAX(numero_calificaciones) ASC;