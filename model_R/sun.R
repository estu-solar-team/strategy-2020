hours <- seq(0+20/60, 23+31/60, 0.0001)

h_radians <- (pi/12) * (hours - (12+26/60))

doy <- 268

decl_radians <- 23.45 * sin(2*pi*(284+doy)/365) * (pi / 180)

lat_radians <- 23.45 * (pi / 180)

sin_gamma <- sin(lat_radians)*sin(decl_radians) + cos(lat_radians)*cos(decl_radians)*cos(h_radians)

m <- 1/sin_gamma


irradiance <- 1353 * sin_gamma * 0.687 ^ (m ^ 0.678)
irradiance[is.na(irradiance)]<-0


plot(hours,irradiance,xlab = 'Saat',ylab = 'Güneş Işınımı {W/m^2}',col=rgb(0.2,0.4,0.1,0.7))


