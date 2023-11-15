from collections import Counter
import matplotlib.pyplot as plt

class Estadisticas:
  @staticmethod
  def informe_publicaciones(usuarios):
    usuarios_publicaciones = Counter([post.usuario for usuario in usuarios for post in usuario.publicaciones])
    usuario_mas_activo = usuarios_publicaciones.most_common(1)
    
    carreras_publicaciones = Counter([usuario.carrera for usuario in usuarios for post in usuario.publicaciones])
    carrera_mas_activa = carreras_publicaciones.most_common(1)

    return usuario_mas_activo, carrera_mas_activa

  @staticmethod
  def informe_interacciones(usuarios, posts):
    interacciones_post = Counter([post for post in posts for _ in post.likes + post.comentarios])
    post_mas_popular = interacciones_post.most_common(1)
    interacciones_usuario = Counter([interaccion.usuario for usuario in usuarios for interaccion in usuario.likes + usuario.comentarios])
    usuario_mas_interactivo = interacciones_usuario.most_common(1)

    return post_mas_popular, usuario_mas_interactivo

  @staticmethod
  def informe_moderacion(usuarios, posts):
    posts_tumbados = Counter([post.usuario for post in posts if post.eliminado])
    usuario_mas_reportado = posts_tumbados.most_common(1)
    carreras_comentarios_inadecuados = Counter([comentario.usuario.carrera for post in posts for comentario in post.comentarios if comentario.eliminado])
    carrera_mas_reportada = carreras_comentarios_inadecuados.most_common(1)

    usuarios_eliminados = [usuario for usuario in usuarios if usuario.eliminado]

    return usuario_mas_reportado, carrera_mas_reportada, usuarios_eliminados

  @staticmethod
  def graficar_estadisticas(estadisticas):
    usuarios, publicaciones = zip(*estadisticas.informe_publicaciones()[0])
    plt.bar(usuarios, publicaciones)
    plt.show()