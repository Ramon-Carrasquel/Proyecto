import datetime

class Post:
  def __init__(self, usuario, multimedia, descripcion, hashtag):
    self.usuario = usuario
    self.multimedia = multimedia
    self.descripcion = descripcion
    self.hashtag = hashtag
    self.fecha_publicacion = datetime.datetime.now()
    self.likes = []
    self.comentarios = []

  def show_attr(self):
    return f"""
    Usuario que publico: {self.usuario}
    Multimedia: {self.multimedia}
    Descripcion: {self.descripcion}
    Hashtag: {self.hashtag}
    Fecha de publicacion: {self.fecha_publicacion}
    """
  
  @staticmethod
  def registrar_nuevo_post(usuario, multimedia, descripcion, hashtag):
    return Post(usuario, multimedia, descripcion, hashtag)

  def mostrar_post(self):
    return [
        self.usuario,
        self.multimedia,
        self.descripcion,
        self.hashtag,
        self.fecha_publicacion,
        self.likes,
        self.comentarios,
    ]

  @staticmethod
  def buscar_posts(posts, filtro, valor):
      return [post for post in posts if getattr(post, filtro) == valor]

  def eliminar_comentario(self, comentario):
    if comentario in self.comentarios:
        self.comentarios.remove(comentario)