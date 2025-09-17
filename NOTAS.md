### Entidades:
#### line => Las diferentes líneas de trenes
#### station => Estaciones de las diferentes líneas
    - Cada línea tiene muchas estaciones
    - Cada estación pertenece a una línea
#### section => Tramos entre estaciones 
    - Una línea tiene muchos tramos
    - Cada tramo pertenece a una línea
#### track => Vías ascendentes, descendentes, etc
    - Cada tramo puede tener varias vías
    - cada vía pertenece a un solo tramo
#### track_direction => La vía es ascendente o descendente
    - Cad vía tiene un sentido
#### subsection => Son subtramos. Se dividen los tramos en subtramos para poder agregar info, por ejemplo, tipos de rieles
    - cada subtramo pertenece a una vía
    - Cada subtramo puede cambiar de tipo de riel
    - Cada subtramo pertenece a un registro historico
#### subsection_rail_type => Registro histórico de los cambios en enrieladura
    - Tabla intermedia donde se relacionan los subtramos con su respectivo tipo de riel registrandose con fecha
#### rail_type => Tipos de rieles, número, descripción
    - Tabla general donde se relaciona la "categoría" del riel con una entidad mas amplia
#### rail_category => Específicamente el número de riel
#### gps point => Puntos GPS
    - Cada subtramo tiene muchos pntos GPS